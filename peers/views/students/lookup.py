from flask import render_template, request, redirect
from peers.server import app
from peers.models import Question
from peers.db import Session

@app.route('/answer')
@app.route('/students/')
def lookup():
    return render_template('students/lookup.html')

@app.route('/lookup', methods=['post'])
@app.route('/students/lookup', methods=['post'])
def do_lookup():
    return redirect('/question/%s' % request.form['question_id'])
