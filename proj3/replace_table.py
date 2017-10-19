import sqlite3

sqlite_file = 'pete.db'
table_name1 = 'posts'
#table_name2 = 'users'  
new_field = 'user'
new_field2 = 'title'
new_field3 = 'post'
new_field4 = 'date_posted'
field_type = 'TEXT'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('''DROP TABLE posts''')

c.execute('''CREATE TABLE posts (user text, title text, post text, date_posted text)''')

conn.commit()

conn.close()


