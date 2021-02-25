from flask import render_template, request, redirect, session

from peers.server import app

@app.route('/admin/logout')
def logout():
    session['logged_in_user'] = None
    return redirect('/login')
