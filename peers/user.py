from flask import session, request
from peers.db import Session
from peers.models import User

def get_username():
    return session.get('logged_in_user')

def get_userid():
    return session.get('logged_in_user_id')
