#!/usr/bin/env python3
class NotSupported(Exception): pass

class Generator(object):
    __trigger = (
        'CREATE OR REPLACE FUNCTION update_{table}_timestamp() '
        'RETURNS TRIGGER AS $$ '
            'BEGIN '
                'NEW.{table}_updated = now(); '
                'RETURN NEW; '
            'END; '
        '$$ LANGUAGE plpgsql; '
        'CREATE TRIGGER tr_{table}_updated BEFORE UPDATE ON {table} '
        'FOR EACH ROW EXECUTE PROCEDURE update_{table}_timestamp();'
    )

    __one_to_many = (
        'ALTER TABLE {child} ADD {parent}_id integer NOT NULL, '
        'ADD CONSTRAINT fk_{child}_{parent}_id ' 
        'FOREIGN KEY ({parent}_id) '
        'REFERENCES {parent} ({parent}_id);'
    )

    __many_to_many_create = (
        'CREATE TABLE {table1}__{table2} ('
            '{table1}_id integer NOT NULL, '
            '{table2}_id integer NOT NULL, '
            'PRIMARY KEY ({table1}_id, {table2}_id)'
        ');'
    )

    __many_to_many_alter = (
        'ALTER TABLE {table1}__{table2} '
            'ADD CONSTRAINT fk_{table1}__{table2}_{table1}_id '
                'FOREIGN KEY ({table1}_id) '
                'REFERENCES {table1} ({table1}_id); '
        'ALTER TABLE {table1}__{table2} '
            'ADD CONSTRAINT fk_{table1}__{table2}_{table2}_id '
                'FOREIGN KEY ({table2}_id) '
                'REFERENCES {table2} ({table2}_id);'
    )

    def __init__(self):
        self.tables = []
        self.triggers = []
        self.relations = []

    def parse(self, name):
        table_relations = []

        with open(name) as file:
            while True:
                line = file.readline().strip().lower()

                if not line:
                    break
                table = line.rstrip(':')
                query = 'CREATE TABLE {table}({table}_id serial PRIMARY KEY, '.format(table=table)
                line = file.readline().strip().lower()
                if line == 'fields:':
                    while True:
                        line = file.readline().strip().lower()

                        if line == 'relations:':
                            while True:
                                line = file.readline().strip().lower()                            
                                if not line:
                                    break
                                _table, relation = line.split(': ')
                                table_relations.append(table)
                                table_relations.append({_table:relation})
                        if not line:
                            break
                        column, _type = line.split(': ')                        
                        query += '{table}_{column} {type}, '.format(
                            table=table, 
                            column=column, 
                            type=_type
                        )
                    query += (
                        '{table}_created timestamp DEFAULT now(), '
                        '{table}_updated timestamp DEFAULT now());'
                    ).format(table=table)
                    self.tables.append(query)
                    self.triggers.append(self.__trigger.format(table=table))
        if table_relations:
            self.built_relations(table_relations)        
        return self.tables + self.relations + self.triggers 

    def built_relations(self, table_relations):
        for i in range(0, len(table_relations), 2): 
            table_1 = table_relations[i]
            table_1_rels = table_relations[i+1]
            for j in range(i+2, len(table_relations), 2):
                table_2 = table_relations[j]
                table_2_rels = table_relations[j+1]
                relation_1 = table_2_rels.get(table_1, False)
                relation_2 = table_1_rels.get(table_2, False)        

                if relation_1 and relation_2:
                    if relation_1 == 'many' and relation_2 == 'many':
                        table_1, table_2 = sorted((table_1, table_2))
                        self.tables.append(self.__many_to_many_create.format(table1=table_1,
                                                                             table2=table_2))
                        self.relations.append(self.__many_to_many_alter.format(table1=table_1,
                                                                               table2=table_2))
                    elif relation_1 == 'many' and relation_2 == 'one':
                        self.relations.append(self.__one_to_many.format(child=table_1, 
                                                                        parent=table_2))
                    elif relation_1 == 'one' and relation_2 == 'many':
                        self.relations.append(self.__one_to_many.format(child=table_2, 
                                                                        parent=table_1))
                    else:
                        raise NotSupported


if __name__ == "__main__":
    generator = Generator()
    for i in generator.parse('yaml.yml'):
        print(i, end='\n\n')
