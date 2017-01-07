# generator

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
