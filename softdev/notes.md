#Notes
**10/28/15**

1. When branch is made on github:

```
git branch gh  //create branch
git checkout gh // switch branch
git pull
git branch --set-upstream-to=origin/gh gh
```
   - the set-upstream command makes it so you can push/pull
   - we don't use this command when we only want to work locally

2. Once we add a new file to the branch, we can "Compare and Pull Request"
   - master is now updated, we can pull and it'll be there

3. Making a new branch in the command line
   - git branch cli
   - you have to then git pull, git upstream, git push -u, etc
   - follow instructions to add the command-line branch to github

4. Merging

```
git checkout master
git pull
git checkout mybranch
git pull
git merge master
git push
*insert work*
commit + push
pull request
```

  - "pull" tries to merge and fetch - type of shorthand
  - "merge" just merges
  - "fetch" just fetches

  - disadvantage of "merge" is that we don't get text comments, comparison, etc
  
---


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
