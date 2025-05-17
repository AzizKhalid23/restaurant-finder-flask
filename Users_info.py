import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')


users = [
    ('Aziz', '1234'),
    ('Mohammed', 'abcd'),
    ('omar', 'pass'),
    ('ahmed', 'test'),
    ('Mazen', 'hello')
]

for user in users:
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", user)
    except:
        pass

conn.commit()
conn.close()