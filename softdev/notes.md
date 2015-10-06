#Notes

**10/6/15**
We're going to be using SQLite3, a library, as a database
Database is a collection of tables

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