
#1
def select_all_one(cur):
   print("Example One:")
   cur.execute("SELECT * FROM movies;")
   movies=cur.fetchall()
   for row in movies:
       print(row)
#2
def select_all_two(cur):
    print("Example two:")
    cur.execute("SELECT * FROM movies;")
    for row in  cur.fetchone():
           print(row)
#3
def select_all_three(cur):
    print("Example three:")
    cur.execute("SELECT * FROM movies;")
    records=cur.fetchall()
    for row in  cur.fetchall():
           print(row)
#4
def insert(cur):
    cur.execute("INSERT INTO movies VALUES (%s, %s)", (9, "Avengers"))
    cur.execute("SELECT * FROM movies;")
    records=cur.fetchall()
    for row in  records:
           print(row)
#5
def select_count_rows(cur):
    cur.execute("SELECT * FROM movies;")
    print(cur.rowcount)
    print (cur.fetchmany(2))
    for row in  cur.fetchmany(2):
           print(row)
    print(cur.rowcount)


