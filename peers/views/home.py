from flask import render_template, redirect
from peers.server import app

@app.route('/')
def home():
    return redirect('/admin/list')
