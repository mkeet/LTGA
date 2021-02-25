from flask import render_template, jsonify
from peers.db import Session
from peers.models import Question, Answer
from peers.server import app
from peers import user

@app.route('/question/data/<int:question_id>')
def question_fetch(question_id):
    try:
        session = Session()
        question = session.query(Question).filter(Question.id == question_id).one()
        answers = sorted(question.current_answers(session), key=lambda x: x.order)
        return jsonify(
                question=question.question,
                potential_answers=[(chr(i+97), a.count) for i, a in enumerate(answers)])
    finally:
        session.close()
