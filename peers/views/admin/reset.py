from flask import render_template, request, redirect
from peers.server import app
from peers.models import Answer, Question
from peers.db import Session

@app.route('/admin/reset/<int:question_id>')
def reset_question(question_id):
    return render_template('confirm.html',
            question='Are you sure you want to reset this question?')

@app.route('/admin/reset/<int:question_id>', methods=['post'])
def do_reset_question(question_id):
    try:
        session = Session()
        if request.form.get('confirm', False):
            session.query(Question) \
                    .filter(Question.id == question_id).one().reset(session)
            session.commit()
        return redirect('/question/%d' % question_id)
    finally:
        session.close()
