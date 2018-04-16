# -*- coding:utf8 -*-
#encoding = utf-8

from . import app
from flask import render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL,MySQLdb
from functools import wraps


# init mysql
mysql = MySQL(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap


# login page
@app.route('/index')
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM acct_mgmt WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['pwd']
            if password_candidate == password:
                # Passed
                session['logged_in'] = True
                session['username'] = username
                cur.close()
                return redirect(url_for('admin.index'))
            else:
                error = 'Password or Username Invalid'
                cur.close()
                return render_template('login.html', error=error)
        else:
            error = 'Password or Username Invalid'
            cur.close()
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    import _mysql_exceptions
    try:
        if mysql.connect.open:
            mysql.connect.close()
    except _mysql_exceptions.DatabaseError:
        print('Closed')
    flash('you are now logged out', 'success')
    return redirect(url_for('index'))
