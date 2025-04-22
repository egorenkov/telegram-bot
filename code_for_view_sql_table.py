import sqlite3

conn = sqlite3.connect('newdb.sql')
c = conn.cursor()

c.execute("""SELECT * FROM comment""")
table = c.fetchall()
c.close()
conn.close()

print('id, user_id, first_name, second_name, commentaris:')
for value_from_table in table:   
    print("{} , {}, {}, {}".format(value_from_table[0],value_from_table[1],
                                   value_from_table[2],value_from_table[3]))

