from flask import render_template, request, redirect, jsonify
from peers.server import app
from peers.models import Question, QuestionGroup
from peers.db import Session
from peers import user

@app.route('/admin/group/create', methods=['post'])
def create_group():
    session = Session()
    try:
        name = request.form.get('group_name')
        group = QuestionGroup(
                name=name,
                user_id=user.get_userid()
                )
        session.add(group)
        session.commit()
        return jsonify({
            'id': group.id,
            'name': group.name
        })
    finally:
        session.close()
