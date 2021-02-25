from flask import render_template, request, redirect
from peers.server import app
from peers.models import Question, QuestionGroup
from peers.db import Session
from peers import user
import json
from datetime import datetime


@app.route('/admin/list', defaults={'page': 0})
@app.route('/admin/list/<int:page>')
def list_questions(page):
    try:
        session = Session()
        groups = session.query(QuestionGroup).filter(
                    QuestionGroup.user_id == user.get_userid()) \
                .order_by(QuestionGroup.group_index) \
                .all()
        groups_jsony=json.dumps([{
            'id':g.id,
            'name':g.name
            } for g in groups])

        questions = Question.my_questions(user.get_userid(), session)
        questions_jsony=json.dumps([{
            'id': q.id,
            'group_id': q.group_id,
            'question': q.question,
            'expired': q.expired,
            'responses': q.num_responses,
            'created_at': q.created_at.strftime('%d %b %Y')
            } for q in questions])
        return render_template(
                'admin/list.html',
                questions=questions_jsony,
                groups=groups_jsony,
                navbar=True)
    finally:
        session.close()
