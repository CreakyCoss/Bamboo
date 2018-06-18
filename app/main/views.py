from . import main
from flask import render_template, redirect, url_for, session
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('username')
    return render_template("index.html", username=username)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data
        session['username'] = username
        return redirect(url_for('.index'))
    return render_template("login.html", form=form)
