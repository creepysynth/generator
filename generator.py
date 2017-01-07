#!/usr/bin/env python
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
        file = open(name)
        mtm_rlts = []

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

                            rel_table, relation = line.split(': ')
                            if relation == 'one':
                                self.relations.append(self.__one_to_many.format(child=table, 
                                                                                parent=rel_table))
                            elif relation == 'many':
                                mtm_rlts.append([table, rel_table])

                    if not line:
                        break

                    column, type = line.split(': ')
                    query += '{table}_{column} {type}, '.format(table=table, 
                                                                column=column, 
                                                                type=type)
                query += ('{table}_created timestamp DEFAULT now(), '
                          '{table}_updated timestamp DEFAULT now());'
                         ).format(table=table)
                self.tables.append(query)
                self.triggers.append(self.__trigger.format(table=table))
        if mtm_rlts:
            self.many_to_many(mtm_rlts)
        
        return self.tables + self.relations + self.triggers 

    def many_to_many(self, relations):
        for i in range(0, len(relations)):
            for j in range(i+1, len(relations)):
                if relations[i][0] == relations[j][1] and relations[i][1] == relations[j][0]:
                    table1, table2 = sorted(relations[i])
                    self.tables.append(self.__many_to_many_create.format(table1=table1,
                                                                         table2=table2))
                    self.relations.append(self.__many_to_many_alter.format(table1=table1,
                                                                           table2=table2))


if __name__ == "__main__":
    generator = Generator()
    for i in generator.parse('yaml.yml'):
        print i, '\n'
