from flask import render_template, request, redirect
from peers.server import app
from peers.models import Question
from peers.db import Session

@app.route('/admin/delete/<int:question_id>')
def delete_question(question_id):
    return render_template('confirm.html',
            question='Are you sure you want to delete this question?')

@app.route('/admin/delete/<int:question_id>', methods=['post'])
def do_delete_question(question_id):
    try:
        session = Session()
        if request.form.get('confirm', False):
            question = session.query(Question).filter(Question.id == question_id).one()
            question.state = 'deleted'
            session.commit()
            return 'Question Deleted'
        else:
            return 'Question not deleted'
    finally:
        session.close()

