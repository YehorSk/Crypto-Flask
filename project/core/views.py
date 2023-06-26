#/core/views.py
from flask import render_template,request,Blueprint,g,session,redirect,url_for
from flask_login import login_user,current_user,logout_user,login_required

from project import db,app,babel
from project import mail
from project.models import User
from project.core.forms import AskForm
import smtplib
from flask_mail import Mail, Message
from random import randint

core = Blueprint('core',__name__)

@babel.localeselector
def get_locale():
     # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    if session.get('language') != None:
        lang = session['language']
        return lang
    return request.accept_languages.best_match(['uk','en'])

@core.route('/lang/<language>')
def set_lang(language):
    session['language'] = language
    return redirect(url_for('core.index'))

@core.route('/', methods=['GET', 'POST'])
def index():
    value = randint(1,5)
    user_id = db.session.query(User).count()
    return render_template('index.html',user_id=user_id,value=str(value))

@core.route('/courses')
@login_required
def courses():
    return render_template('courses.html')
