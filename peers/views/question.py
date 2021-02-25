from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from flask import render_template, request
from peers.db import Session
from peers.models import Question, Run
from peers.server import app
from peers.views.question_fetch import question_fetch
from peers import user

@app.route('/question/<question_id>')
def show_question(question_id):
    answered_questions = map(int, request.cookies.get('answered-questions', '-1').split(','))
    if question_id in answered_questions:
        return 'You have already answered this question'
    try:
        int(question_id)
    except ValueError:
        return render_template(
                'students/lookup.html',
                error='Question ID must be a number')
    session = Session()
    try:
        question = session.query(Question).filter(Question.id == question_id).one()

        answers = []
        for i, x in enumerate(sorted(question.current_answers(session), key=lambda x: x.id)):
            answers.append('%s) %s' % (chr(ord('a')+i), x.answer))

        chartData = question_fetch(question_id).data
        return render_template('question.html',
                question=question,
                answers=answers,
                chartData=chartData,
                expired=question.expired)
    except NoResultFound:
        return render_template(
                'students/lookup.html',
                error='Question with id %d not found' % int(question_id))
    finally:
        session.close()
