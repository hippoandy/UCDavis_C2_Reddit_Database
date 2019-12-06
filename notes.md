# MySQL (MariaDB) Learning Notes

## "mysqldump" Usage

### Get the Database Schema

```bash
$ mysqldump --xml --no-data --single-transaction=true -h <host> -u <account> -p <database_name> > /tmp/schema.xml
```

## References

### ASCII Table

* [http://www.asciitable.com/](http://www.asciitable.com/)

### Optimization

* [https://dzone.com/articles/how-to-optimize-mysql-queries-for-speed-and-perfor](https://dzone.com/articles/how-to-optimize-mysql-queries-for-speed-and-perfor)

### Index

*[https://stackoverflow.com/questions/5719392/why-isnt-mysql-using-any-of-these-possible-keys](https://stackoverflow.com/questions/5719392/why-isnt-mysql-using-any-of-these-possible-keys)

### Create CSV

* [https://database.guide/how-to-save-a-mysql-query-result-to-a-csv-file/](https://database.guide/how-to-save-a-mysql-query-result-to-a-csv-file/)
* [https://mariadb.com/kb/en/library/select-into-outfile/](https://mariadb.com/kb/en/library/select-into-outfile/)

### Server Out of Memory

* [https://bobcares.com/blog/mysqld-out-of-memory/](https://bobcares.com/blog/mysqld-out-of-memory/)

### Client Out of Memory

* [https://dev.mysql.com/doc/refman/8.0/en/out-of-memory.html](https://dev.mysql.com/doc/refman/8.0/en/out-of-memory.html)

### Foreign Key Constrain

* [https://www.w3schools.com/sql/sql_foreignkey.asp](https://www.w3schools.com/sql/sql_foreignkey.asp)

### SQL - Analyze Table

* [https://dev.mysql.com/doc/refman/5.6/en/analyze-table.html]()

### SQL - Alter Column

```sql
ALTER TABLE <table_name> MODIFY COLUMN <col_name> <col_type> NOT NULL;
```

* [https://dba.stackexchange.com/questions/152387/altering-a-column-null-to-not-null](https://dba.stackexchange.com/questions/152387/altering-a-column-null-to-not-null)

### SQL - Length of Value

* [https://stackoverflow.com/questions/1545467/mysql-select-statement-for-the-length-of-the-field-is-greater-than-1](https://stackoverflow.com/questions/1545467/mysql-select-statement-for-the-length-of-the-field-is-greater-than-1)

### SQL - Value IS LIKE

* [https://stackoverflow.com/questions/6447899/select-where-row-value-contains-string-mysql](https://stackoverflow.com/questions/6447899/select-where-row-value-contains-string-mysql)

### SQL - Append Text to Value

* [https://stackoverflow.com/questions/16965011/append-text-to-each-row-of-the-sql-select-query](https://stackoverflow.com/questions/16965011/append-text-to-each-row-of-the-sql-select-query)

### SQL - Replace Char in Value

* [https://stackoverflow.com/questions/2259446/need-to-export-fields-containing-linebreaks-as-a-csv-from-sql-server/11330194](https://stackoverflow.com/questions/2259446/need-to-export-fields-containing-linebreaks-as-a-csv-from-sql-server/11330194)

### SQL - String not equal

* [https://stackoverflow.com/questions/16324504/sql-how-to-perform-string-does-not-equal](https://stackoverflow.com/questions/16324504/sql-how-to-perform-string-does-not-equal)