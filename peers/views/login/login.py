from flask import render_template, request, redirect
from flask import session as flask_session
from peers.server import app
from peers.db import Session
from peers.models import User

available_urls = [
    'register',
    'do_register',
    'student_answer',
    'do_student_answer',
    'lookup',
    'do_lookup',
    'image',
    'login',
    'perform_login',
    'static',
    'show_question'
    ]

@app.before_request
def assert_login():
    if not request.url_rule:
        return
    print request.url_rule.endpoint
    free_for_all = request.url_rule.endpoint in available_urls
    print free_for_all
    if not flask_session.get('logged_in_user', None) and not free_for_all:
        return redirect('/login')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/do_login', methods=['post'])
def perform_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        print 'error'
        return render_template('login.html', error=True)

    session = Session()
    user = User.login(username, password, session)
    if user is None:
        print 'error'
        return render_template('login.html', error=True)

    flask_session['logged_in_user'] = user.username
    flask_session['logged_in_user_id'] = user.id
    return redirect('/')
