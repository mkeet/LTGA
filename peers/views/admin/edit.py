from flask import render_template, request, redirect
from peers.server import app
from peers.models import Question, Run
from peers.db import Session
from peers.views.images import upload_image

@app.route('/admin/edit/<int:question_id>')
def edit_question(question_id):
    try:
        session = Session()
        question = session.query(Question).filter(Question.id == question_id).one()
        potential_answers = '[%s]' % ', '.join('"%s"' % a.answer.replace('\\', '\\\\') for a in question.current_answers(session))
        return render_template(
                'edit_question.html',
                question=question,
                potential_answers=potential_answers,
                navbar=True)
    finally:
        session.close()

@app.route('/admin/edit/<int:question_id>', methods=['post'])
def do_edit_question(question_id):
    num_answers = sum(1 for k in request.form if k.startswith('answer'))
    answers = [request.form['answer%d'%x] for x in xrange(num_answers)]
    try:
        session = Session()
        question = session.query(Question).filter(Question.id==question_id).one()
        answers = sorted([(int(k[len('answer'):]), ans)
                for k, ans in request.form.iteritems()
                if k.startswith('answer') and ans])

        image_filename = question.image_filename
        if 'question-image' in request.files and request.files['question-image'].filename:
            image_filename = request.files['question-image'].filename
            upload_image('question-image')

        question.update(request.form['question'], answers, image_filename, session)
        return redirect('/question/%d' % question_id)
    finally:
        session.close()

