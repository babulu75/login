from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Secret key and database config (use environment variables for sensitive data)
app.secret_key = 'Babulu@8520'  # Replace with a strong, unique secret key
app.config['MYSQL_HOST'] = 'localhost'  # Keep localhost if MySQL is running locally
app.config['MYSQL_USER'] = 'root'  # MySQL username, typically 'root'
app.config['MYSQL_PASSWORD'] = 'Vinni@02#feb'  # Replace with your actual MySQL root password
app.config['MYSQL_DB'] = 'geeklogin'  # Ensure this matches your database name


mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and bcrypt.check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('index.html', msg='Logged in successfully!')
        else:
            msg = 'Incorrect username or password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        email_account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif email_account:
            msg = 'Email already registered!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hashed_password, email))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                return redirect(url_for('login'))
            except MySQLdb.Error as e:
                msg = f'An error occurred: {e}'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
