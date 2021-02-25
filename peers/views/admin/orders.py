from flask import render_template, request, redirect, jsonify
from peers.server import app
from peers.models import Question, QuestionGroup
from peers.db import Session
from peers import user

@app.route('/admin/order', methods=['post'])
def update_order():
    session = None
    update_type = request.form.get('type')
    from_id = request.form.get('from_id')
    to_id = request.form.get('to_id')
    try:
        session = Session()
        if update_type == 'new_group_question':
            from_question = session.query(Question) \
                    .filter(Question.user_id == user.get_userid()) \
                    .filter(Question.id == from_id) \
                    .one()
            from_question.group_id = to_id
            from_question.group_index = 1
            session.add(from_question)
            session.commit()

            return jsonify({'success': True})

        elif update_type == 'question':
            from_question = session.query(Question) \
                    .filter(Question.user_id == user.get_userid()) \
                    .filter(Question.id == from_id) \
                    .one()
            to_question = session.query(Question) \
                    .filter(Question.user_id == user.get_userid()) \
                    .filter(Question.id == to_id) \
                    .one()
            to_question_index = to_question.group_index

            # if both questions in the same group
            if to_question.group_id == from_question.group_id:
                # if from was below "to question" we have to move "to question" down
                if from_question.group_index > to_question.group_index:
                    to_question.group_index += 1
                # if from was above "to question" we have to move "to question" up
                else:
                    to_question.group_index -= 1
            # if the questions are in different groups
            else:
                raise Exception('we do not handle this yet')

            session.add(to_question)

            print 'YAAAAAAAAAy'
            from_question.group_index = to_question_index
            session.add(from_question)
            session.commit()
            return jsonify({'success': True})
        else:
            raise Exception('unknown type')
    finally:
        session.close()
