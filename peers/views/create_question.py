from flask import render_template, request, redirect, session
from peers.server import app
from peers.models import Question
from peers.views.images import upload_image
from peers import user

@app.route('/create_question')
def create_question():
    return render_template('create_question.html', navbar=True)

@app.route('/create_question', methods=['post'])
def do_create_question():
    answers = [ans for k, ans in sorted(request.form.iteritems()) if k.startswith('answer') and ans]
    image_filename = None
    if 'question-image' in request.files:
        image_filename = request.files['question-image'].filename
        upload_image('question-image')
    question = request.form['question']
    question_id = Question.create(user.get_userid(), question, answers, image_filename)

    return redirect('/question/%d' % question_id)
