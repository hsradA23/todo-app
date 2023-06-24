# Todo App
This is a simple Todo application built using Flask, SQLite, and Svelte. The application supports user authentication, and allows users to add, edit, delete, and filter tasks.

# Features
- **Flask** is used to provide the backend for the webapp.

- **SvelteJS** is used for the frontend

- **SQLite3** is used to create a relational database and run queries

- User authentication: Users can create an account, log in, and log out.

- Task management: Users can add new tasks, mark tasks as completed, edit task details, and delete tasks.

- Task filtering: Users can filter tasks based on their status (completed or active).

## Frontend
As the fontend is a SvelteJS project, It has a different [repository](https://github.com/hsradA23/todo-frontend).

# Files
`app.py` : The Flask API

`sql_helper.py` : Functions used to interact with the database

# API endpoints

- `/static/*` : Used to serve the html and js files

- `/api/todo/add` : Add a task

- `/api/todo/get` : Query users' tasks

- `/api/todo/update` : Modify a task

- `/api/todo/done` : Change the done status of the task

- `/api/todo/delete` : Delete a task

- `/login` : Login to an account

- `/register` : Create a new user

# How to run

- Clone the repo.

- `pip install -r requirements.txt` to download the packages.

- `flask --app app run` to start the server.

- Navigate to `http://127.0.0.1:5000/` with a web browser.