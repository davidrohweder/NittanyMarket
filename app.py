# *************************************** SETUP

from flask import Flask, redirect, render_template, request
import sqlite3 as sql

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

# *************************************** END SETUP


# default intructions: on host url return default index
@app.route('/')
def index():
    return render_template('index.html')


# on patient portal (POST: check value of form on page if add then redirect to add otherwise redirect to delete) no action return page
@app.route('/patientportal', methods=['POST', 'GET'])
def patientportal():
    error = None
    if (request.method == 'POST'):
        result = request.form.get('selection')
        if (result == 'add'):
            return redirect('/add')
        else:
            return redirect('/delete')
    else:
        return render_template('patientportal.html', error=error)


# on delete (POST: AMBIGUOUS INSTRUCTIONS so delete pid to delete user on pid) on default load table with all results from users if delete reprint new table on no action return page
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    error = None
    result = delete_preview()
    if request.method == 'POST':
        delete_request(request.form['FirstName'], request.form['LastName'])
        if result:
            result = delete_preview()
            return render_template('delete.html', error=error, result=result)
        else:
            error = 'invalid input pid'
    return render_template('delete.html', error=error, result=result)

def delete_request(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    connection.execute('DELETE FROM users WHERE firstname =''?'' AND lastname =''?'' ', (first_name, last_name) )
    connection.commit()

def delete_preview():
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()


# on add (POST: add usr to table with FN and LN) on no action return pages
@app.route('/add', methods=['POST', 'GET'])
def add():
    error = None
    if request.method == 'POST':
        result = add_request(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('add.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('add.html', error=error)


def add_request(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()


# default instructions
if __name__ == "__main__":
    app.run()