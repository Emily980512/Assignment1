from crypt import methods
import sqlite3
from flask import Flask, Response, request
import uuid
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST','GET'])
def createTask():
    conn = get_db_connection()
    if request.method == 'POST':
        task = request.get_json()
        print("This is task: ", task)
        try:
            task_id = random.randint(1,10000000000)
            title, is_completed = task['title'], task['is_completed']
            print(title)
            print(is_completed)
            conn.execute('INSERT INTO tasks_3034504344 (id, title, is_completed) VALUES (?, ?, ?)',
                     (task_id, title, is_completed))
            # cursor = conn.cursor()
            # lastRowId = cursor.lastrowid
            conn.commit()
            conn.close()
            return {'id': task_id}, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    else:
        tasks = conn.execute('SELECT * FROM tasks_3034504344').fetchall()
        # print('Type: ', tasks)
        conn.close()
        taskList = list()
        for task in list(tasks):
            taskList.append({
                'id': task['id'],
                'title': task['title'],
                'is_completed': task['is_completed']
            })
        return {'tasks': taskList}, 200 

@app.route('/<string:id>/', methods=['GET', 'PUT', 'DELETE'])
def getById(id):
    conn = get_db_connection()
    if request.method == 'GET':
        task = conn.execute('SELECT * FROM tasks_3034504344 WHERE id = ?',
                        (id,)).fetchone()
        conn.close()
        if task is None:
                return {'error': 'Invalid ID', 'status': 400}, 400
        return {'task': {
                'id': task['id'],
                'title': task['title'],
                'is_completed': task['is_completed'],
                }}, 200
    elif request.method == 'PUT':
        task = request.get_json()
        try:
            title, is_completed = task['title'], task['is_completed']
            conn.execute('UPDATE tasks_3034504344 SET title = ?, is_completed = ? WHERE id = ?', 
                    (title, is_completed, id))
            conn.commit()
            # task = conn.execute('SELECT * FROM tasks_3036434871 WHERE id = ?', (id,)).fetchone()
            conn.close()
            return {}
        except:
            return {}
    else:
        conn.execute('DELETE FROM tasks_3034504344 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return {}

