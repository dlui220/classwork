#Notes

**10/6/15**


We're going to be using SQLite3, a library, as a database

--Database is a collection of tables

```sql	  
--anything with a '.' in front is not a sql statement.
--instead, it is a sqlite3 statement. Ex: '.help'

.open doughnutstore.db
.databases

--the database is a collection of tables

.tables
CREATE TABLE doughnuts (name text, price real, qty integer); 
--all sql statements end with a semicolon

--traditionally, SQL statements are in uppercase.

```

---

**10/1/15**

```Python
f = open("data.dat",'w')
f.write("HELLO\n")
f.close()

f = f.open("data.dat","r")
s = f.read()
s = f.readline()
print s
for l in f.readline():
    print l

s = f.readlines()
print s

import shelve
d = {}
d = shelve.open("shelf.dat")
```