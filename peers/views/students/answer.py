from datetime import datetime
from flask import render_template, request, redirect, session as flask_session

from peers.server import app
from peers.models import Question, Answer, Run
from peers.db import Session

def can_user_answer(question_id, run_id):
    return '%d-%d' % (question_id, run_id) not in flask_session.get('answered_questions', '').split()

@app.route('/students/question/<int:question_id>')
def student_answer(question_id):
    try:
        session = Session()
        question = session.query(Question).filter(Question.id == question_id).one()
        answers = sorted(question.current_answers(session), key=lambda x: x.id)
        if question.expired:
            return render_template('students/closed.html')
        if not can_user_answer(question_id, question.current_run_id):
            return render_template('students/already_voted.html')
        return render_template('students/answer.html', question=question, run=question.current_run(session))
    finally:
        session.close()

@app.route('/students/answer/<int:question_id>', methods=['post'])
@app.route('/answer/<int:question_id>', methods=['post'])
def do_student_answer(question_id):
    try:
        session = Session()
        question = session.query(Question).filter(Question.id == question_id).one()
        if question.expired:
            return render_template('students/closed.html')
        if not can_user_answer(question_id, question.current_run_id):
            return render_template('students/already_voted.html')
        for answer in question.current_answers(session):
            if answer.answer == request.form['answer']:
                requested_answer = answer
                break
        else:
            raise Exception('no answer, weird')
        requested_answer.count = Answer.count + 1
        flask_session['answered_questions'] = flask_session.get('answered_questions', '')+' %d-%d' % (question_id, question.current_run_id)
        session.add(requested_answer)
        session.commit()
        return render_template('students/congrats.html')
    finally:
        session.close()
