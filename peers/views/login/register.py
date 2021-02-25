from flask import render_template, request, redirect
from flask import session as flask_session
from peers.server import app
from peers.db import Session
from peers.models import User

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['post'])
def do_register():
    username = request.form.get('username')
    password = request.form.get('password')
    password_verify = request.form.get('password_verify')

    session = Session()
    try:
        count = session.query(User).filter(User.username == username).count()
        if count != 0:
            error = 'Username already exists'
            return render_template('register.html', error=error)

        if len(password) < 5:
            error = 'Password needs to be at least 5 characters'
            return render_template('register.html', error=error, username=username)

        print password, password_verify

        if password != password_verify:
            error = 'Passwords do not match'
            return render_template('register.html', error=error, username=username)

        user = User.register(username, password, session)

        flask_session['logged_in_user'] = user.username
        flask_session['logged_in_user_id'] = user.id
        return redirect('/admin/list')
    finally:
        session.close()
