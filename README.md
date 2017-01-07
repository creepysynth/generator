# generator

Пример схемы:

Article:</br>
&nbsp;fields:</br>
&nbsp;&nbsp;title: varchar(50)</br>
&nbsp;&nbsp;text: text</br>
&nbsp;relations:</br>
&nbsp;&nbsp;Category: one</br>
&nbsp;&nbsp;Tag: many</br>
</br>
Category:</br>
&nbsp;fields:</br>
&nbsp;&nbsp;title: varchar(50)</br>
&nbsp;relations:</br>
&nbsp;&nbsp;Article: many</br>
</br>
Tag:</br>
&nbsp;fields:</br>
&nbsp;&nbsp;value: varchar(50)</br>
&nbsp;relations:</br>
&nbsp;&nbsp;Article: many</br>
