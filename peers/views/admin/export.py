from flask import render_template, request, redirect, Response
from peers.server import app
from peers.models import Question, Run
from peers.db import Session

@app.route('/admin/export/<int:question_id>.csv')
def export(question_id):
    ''' export a csv with the format

    question, answer, run_created, count'''
    rows = [('Answer', 'Count', 'Question', 'Run', )]
    try:
        session = Session()
        question = session.query(Question).filter(Question.id == question_id).one()
        runs = session.query(Run).filter(Run.question_id == question_id).all()
        runs = sorted(runs, key=lambda x: x.id)
        for run in runs:
            for answer in run.answers:
                rows.append((
                    answer.answer,
                    answer.count,
                    question.question,
                    run.id
                    ))
        csv = '\n'.join(', '.join('"%s"' % str(a) for a in row) for row in rows)
        return Response(csv, content_type='text/csv')
    finally:
        session.close()
