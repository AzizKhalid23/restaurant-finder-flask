from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']
restaurants = db['restaurants']

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'project_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            session['logged_in'] = True
            return redirect(url_for('search'))
        else:
            session['logged_in'] = False
            error = 'The information is not correct'
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            message = 'Username already exists.'
            conn.close()
    return render_template('signup.html', message=message)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    result = None
    no_result = False

    if request.method == 'POST':
        query = {}
        if request.form['street']:
            query['address.street'] = {'$regex': request.form['street'], '$options': 'i'}
        if request.form['borough']:
             query['borough'] = {'$regex': request.form['borough'], '$options': 'i'}
        if request.form['cuisine']:
             query['cuisine'] = {'$regex': request.form['cuisine'], '$options': 'i'}
        if request.form['grade']:
            query['grades.grade'] = {'$regex': request.form['grade'], '$options': 'i'}
        if request.form['name']:
            query['name'] = {'$regex': request.form['name'], '$options': 'i'}

        result = list(restaurants.find(query))
        if not result:
            no_result = True

    return render_template('page2.html', result=result, no_result=no_result)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
