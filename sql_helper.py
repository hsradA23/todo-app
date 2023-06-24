# This file contains functions used to interact with the SQL database

import sqlite3 as sl

def init_database(con, cursor):
    # User Table | id is userid unique for every user
    sql_statement = '''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR NOT NULL UNIQUE,
                        pass VARCHAR NOT NULL
                    )'''
    cursor.execute(sql_statement)
    # Tasks Table
    # tid  - is task id
    # id   - is userid, used to create a relation with the users table
    # done - whether the task is already done(1 = task done)
    # text - the task data
    # deadline - deadline for the task
    # added - when was the task added
    sql_statement = '''CREATE TABLE IF NOT EXISTS todo (
        tid INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER NOT NULL,
        done INTEGER CHECK (done IN (0, 1)) DEFAULT 0,
        text VARCHAR,
        deadline DATE,
        added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(sql_statement)
    con.commit()


def add_user(con, cursor, uname, passHash):
    # Adds a user to the database
    # returns 1 on success, 0 on faliure
    # Faliure can occor when the username is taken
    try:
        sql_statement = f'''INSERT INTO users (name,pass)
                        VALUES ( '{uname}', '{passHash}');'''
        cursor.execute(sql_statement)
        con.commit()
    except:
        return 0
    return 1


def verify_user(con, cursor, uname, passHash):
    # Verifies user.
    # This compares the stored password hash to the new hash.
    # It is safe because the actual password never leaves the browser,
    # only the hashes are compared on the server.
    # Returns the user id on success, -1 on faliure
    sql_statement = f'''SELECT id,pass FROM users WHERE name='{uname}';'''
    cursor.execute(sql_statement)
    databaseOutput = cursor.fetchone()
    if(databaseOutput == None): return -1
    return databaseOutput[0] if databaseOutput[1] == passHash else -1


def add_task(con, cursor, uname,passHash , text, deadline):
    # Verifies the user and adds a task into the todo table
    uid = verify_user(con, cursor, uname, passHash)

    sql_statement = f'''INSERT INTO todo (id,text,deadline)
                        VALUES ( '{uid}', '{text}', '{deadline}');'''
    cursor.execute(sql_statement)
    con.commit()


def get_users_tasks(con, cursor, uname,passHash,filter,search):
    # Verifies the user and sends a list of tasks using JOIN operations
    # in the relational database.
    uid = verify_user(con, cursor, uname, passHash)
    print(filter)
    sql = f'''SELECT tid, done, text,deadline
                    FROM todo a, users b
                    WHERE a.id = b.id AND a.id='{uid}' '''
    if(filter == 'Done'):
        sql += ''' AND done = 1 '''
    elif(filter == 'Pending'):
        sql += ''' AND done = 0 '''

    if(search != ''):
        sql += f''' AND text LIKE '%{search}%' '''

    sql+=''' ORDER BY done ASC, added DESC;'''

    cursor.execute(sql)
    databaseOutput = cursor.fetchall()

    return databaseOutput


def update_text(con, cursor, uname,passHash,tid, newText):
    # Change the text stored in the database
    sql_statement = f'''UPDATE todo SET text='{newText}' WHERE tid={tid};'''
    cursor.execute(sql_statement)
    con.commit()

def done_task(con, cursor, tid):
    # Change the status of the task, 1 to 0 or 0 to 1
    sql_statement = f'''UPDATE todo SET done = CASE WHEN done = 0 THEN 1 ELSE 0 END WHERE tid={tid};'''
    cursor.execute(sql_statement)
    con.commit()

def delete_task(con,cursor,tid):
    # Delete task with the given id
    sql_statement = f'''DELETE FROM todo WHERE tid={tid};'''
    cursor.execute(sql_statement)
    con.commit()


# init_database(con,cursor)
# print(add_user(con, cursor, "adarsh", '1234'))
# print(verify_user(con, cursor, 'adarsh','1234'))
# add_task(con, cursor, 'adarsh','1234','Sleep.','deadline')
# print(get_users_tasks(con, cursor, "adarsh", '1234'))


