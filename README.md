# generator

Сгенерировать DDL из схемы БД, заданной в формате YAML. На первом уровне схема содержит лишь названия сущностей и поля с типами.
Конечному пользователю нужен примерно один метод (функция), который возвращает список стрингов со стейтментами, приняв имя файла со схемой.

Пример схемы:

Article:</br>
&nbsp;&nbsp;&nbsp;&nbsp;fields:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;title: varchar(50)</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;text: text</br>
&nbsp;&nbsp;&nbsp;&nbsp;relations:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Category: one</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tag: many</br>
</br>
Category:</br>
&nbsp;&nbsp;&nbsp;&nbsp;fields:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;title: varchar(50)</br>
&nbsp;&nbsp;&nbsp;&nbsp;relations:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Article: many</br>
</br>
Tag:</br>
&nbsp;&nbsp;&nbsp;&nbsp;fields:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;value: varchar(50)</br>
&nbsp;&nbsp;&nbsp;&nbsp;relations:</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Article: many</br>
</br>
**Feature: one_to_many**</br>
Добавляется поддержка 1:m отношений между сущностями. Отношения сущности самой с собой не поддерживать. Проверять парность отношений: например, для отношения Article->Category (one) следует убедиться, что существует Category->Article (many). Ожидаемый результат дополняется полем category_id (и внешним ключом) в таблице article.

**Feature: many_to_many**</br>
Добавляется поддержка m:m отношений между сущностями. Отношения сущности самой с собой не поддерживать. Как и прежде, проверять парность отношений. Имена связующих таблиц формировать в формате table1_table2 (имена таблиц в порядке по возрастанию). Ожидаемый результат дополняется таблицей tag и связующей таблицей article_tag. 
