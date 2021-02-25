from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import column
from sqlalchemy import Table
from datetime import datetime
import hashlib

from peers.db import Base, Session
from peers import UserError

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)

    @staticmethod
    def hash_password(password):
        hash = hashlib.sha1()
        hash.update(password)
        password_hash = hash.hexdigest()
        return password_hash


    @staticmethod
    def login(username, password, session):
        try:
            password_hash = User.hash_password(password)
            user = session.query(User) \
                .filter(username == User.username) \
                .filter(password_hash == User.password_hash) \
                .one()
        except NoResultFound:
            return None

        return user

    @staticmethod
    def register(username, password, session):
        user_count = session.query(User) \
                .filter(username == User.username) \
                .count()
        if user_count > 0:
            raise UserError('A user exists with this name')

        password_hash = User.hash_password(password)
        user = User(
            username=username,
            password_hash=password_hash)
        session.add(user)
        session.flush()
        question_group = QuestionGroup(
                name='Uncategorised',
                user_id=user.id)
        session.add(question_group)
        session.commit()
        return user




class QuestionGroup(Base):
    __tablename__ = 'question_group'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('question_groups'))
    name = Column(String)
    # the order in which groups should appear
    group_index = Column(Integer)

class Question(Base):
    __tablename__ = 'question'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('questions'))
    id = Column(Integer, primary_key=True)
    image_filename = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    state = Column(Enum('active', 'deleted', name='state'), default='active')
    type = Column(Enum('multiple-choice', 'open-ended', name='type'))
    current_run_id = Column(Integer)

    group_id = Column(Integer, ForeignKey('question_group.id'))
    # position within the group
    group_index = Column(Integer)

    opens_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)

    question = Column(String)

    def current_run(self, session):
        run = session.query(Run) \
                .filter(Run.id == self.current_run_id) \
                .one()
        return run

    @property
    def num_responses(self):
        try:
            session = Session()
            return sum(a.count for a in self.current_answers(session))
        finally:
            session.close()


    def current_answers(self, session):
        run = session.query(Run) \
                .filter(Run.id == self.current_run_id) \
                .one()
        return run.answers

    @staticmethod
    def my_questions(user_id, session):
        return session.query(Question) \
                .filter(Question.state == 'active') \
                .filter(Question.user_id == user_id) \
                .order_by(Question.group_index) \
                .all()


    @property
    def expired(self):
        return self.expires_at and self.expires_at <= datetime.now()

    @staticmethod
    def create(user_id, question, answers, image_filename=None):
        try:
            session = Session()

            question_group = session.query(QuestionGroup) \
                    .filter(QuestionGroup.user_id==user_id) \
                    .filter(QuestionGroup.name == 'Uncategorised') \
                    .one()

            question = Question(
                    question=question,
                    image_filename=image_filename,
                    user_id=user_id,
                    group_id=question_group.id)
            session.add(question)
            session.commit()

            run = Run(question_id=question.id, run=0, user_id=user_id)
            session.add(run)
            session.commit()
            question.current_run_id = run.id
            session.add(question)

            for i, a in enumerate(answers):
                session.add(Answer(
                    answer=a,
                    question=question,
                    run_id=run.id,
                    order=i))
            session.commit()
            return question.id
        finally:
            session.close()

    def update(self, question, answers, image_filename, session=None):
        try:
            if not session:
                session = Session()

            previous_run = session.query(Run) \
                    .filter(Run.id == self.current_run_id) \
                    .one()
            run = Run(
                    question_id=self.id,
                    run=previous_run.run+1)
            session.add(run)
            session.commit()
            self.current_run_id = run.id

            for i, a in enumerate(answers):
                count= 0 if i >= len(previous_run.answers) else previous_run.answers[i].count
                session.add(Answer(
                    answer=a[1],
                    question=self,
                    run_id=run.id,
                    count=count,
                    order=a[0]))
            self.image_filename = image_filename

            self.question = question
            session.add(self)
            session.commit()
        finally:
            session.close()

    def reset(self, session=None):
        if not session:
            session = Session()

        previous_run = session.query(Run) \
                .filter(Run.id == self.current_run_id) \
                .one()
        old_answers = previous_run.answers

        run = Run(
                question_id = self.id,
                run = previous_run.run+1,
                user_id = previous_run.user_id)
        session.add(run)
        session.commit()

        self.current_run_id = run.id
        session.add(self)

        for i, a in enumerate(old_answers):
            session.add(Answer(
                order=a.order,
                answer=a.answer,
                question=self,
                run_id=run.id))
        session.add(self)
        session.commit()

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    order = Column(Integer, nullable=False)

    question = relationship('Question', backref=backref('answers'))
    question_id = Column(Integer, ForeignKey('question.id'))
    answer = Column(String)

    count = Column(Integer, default=0)
    run_id = Column(Integer, ForeignKey('run.id'))
    run = relationship('Run', backref=backref('answers'))


class Run(Base):
    __tablename__ = 'run'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now)

    run = Column(Integer)

from peers import  user
