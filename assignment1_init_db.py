import sqlite3
import uuid
import random
import sys

connection = sqlite3.connect('database.db')

newTaskId = random.randint(1,sys.maxsize)


with open('Assignment1_Schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


cur.execute("INSERT INTO tasks_3034504344 (id, title, is_completed) VALUES (?, ?, ?)",
            (newTaskId, "First Test", "False")
            )

connection.commit()
connection.close()