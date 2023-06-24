from flask import Flask, request, send_from_directory, redirect, url_for
from json import dumps
import sqlite3 as sl
from sql_helper import *

app = Flask(__name__)

con = sl.connect('todo.db', check_same_thread=False)
cursor = con.cursor()

init_database(con,cursor)


# Redirect to index.html
# http://127.0.0.1:5000/static/index.html
@app.route("/")
def index():
    return redirect(url_for('serve_static', filename='index.html'))


# Send all the static HTML, JS and CSS files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Verify the user's identity and add a task
@app.route('/api/todo/add', methods=['POST'])
def handle_add():
    data = request.json  
    add_task(con,cursor,data['user'],data['token'],data['newtodo'],data['date'])
    return 'Success'

# Verify the user's identity and get their tasks
# Uses the parameters username, passwordm, filters, search term
@app.route('/api/todo/get', methods=['POST'])
def handle_get():
    data = request.json  
    t = get_users_tasks(con,cursor,data['user'],data['token'],data['doneFilter'],data['searchTerm'])
    return dumps(t)

# Verify the user's identity and Update their task
# Uses the parameters username, passwordm, task_id, updated text
@app.route('/api/todo/update', methods=['POST'])
def handle_updatetext():
    data = request.json  
    update_text(con,cursor,data['user'],data['token'],
                    data['tid'],data['newValue'])
    return 'Successful'

# Change whether a task has been completed
# Uses the parameters task_id
@app.route('/api/todo/done', methods=['POST'])
def handle_done():
    data = request.json  
    done_task(con,cursor,data['tid'])
    return 'Successful'

# Delete a task
# Uses the parameters task_id
@app.route('/api/todo/delete', methods=['POST'])
def handle_delete():
    data = request.json  
    delete_task(con,cursor,data['tid'])
    return 'Successful'

# Verify the credientials from the user
# Uses the parameters username and password
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json  
    o = verify_user(con,cursor,data['user'],data['token'])
    return 'Successful' if o > 0 else "Failure"

# Add a new user to the database
# Uses the parameters username and password
@app.route('/register', methods=['POST'])
def handle_register():
    data = request.json  
    o = add_user(con,cursor,data['user'],data['token'])
    return 'Successful' if o == 1 else "Failure"
