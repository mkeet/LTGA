from datetime import datetime
from flask import render_template, request, redirect
from peers.server import app
from peers.models import Question
from peers.db import Session

@app.route('/admin/open/<int:question_id>')
def open(question_id):
    session = Session()
    try:
        question = session.query(Question).filter(Question.id == question_id).one()
        question.expires_at = None
        session.add(question)
        session.commit()
        return redirect('/question/%d' %  question_id)
    finally:
        session.close()


@app.route('/admin/close/<int:question_id>')
def close(question_id):
    session = Session()
    try:
        question = session.query(Question).filter(Question.id == question_id).one()
        question.expires_at = datetime.now()
        session.add(question)
        session.commit()
        return redirect('/question/%d' %  question_id)
    finally:
        session.close()
