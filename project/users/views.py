#users/views.py
from flask import Flask,render_template,url_for,flash,redirect,request,Blueprint,session,g,session
from flask_login import login_user,current_user,logout_user,login_required
from project import db,s,mail,app,admin,babel
from project.models import User
from project.users.forms import RegistrationForm,LoginForm,UpdateUserForm,AskForm,ChangePasswordForm,ForgotPasswordForm
from project.users.picture_handler import add_profile_pic
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
from flask_admin.contrib.sqla import ModelView

users = Blueprint('users',__name__)

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

@users.route('/lang/<language>')
def set_lang(language):
    session['language'] = language
    return redirect(url_for('users.index'))

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))



@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    confirmed=False)
        db.session.add(user)
        db.session.commit()
        email=form.email.data
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender ='crypto.course.help@gmail.com',recipients=[email])
        link = url_for('confirm_email',token=token,_external=True)
        msg.body = f'Your link is {link}'

        mail.send(msg)
        session['email'] = email
        session['token'] = token
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('signup.html',form=form)

@app.route('/confirm/<token>')
def confirm_email(token):

    try:
       email = s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:


        return 'The token is expired'


    current_user.confirmed = True
    db.session.commit()
    return render_template('thanks.html',email = email)

@app.route('/welcome')
def welcome():
	activate = False
	if 'email' in session and 'token' in session:
		email = session['email']
		token = session['token']

		return render_template('welcome.html',email=email,token=token)
	else:
		return redirect(url_for('index'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@users.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login success!')

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)


    return render_template('login.html',form=form)


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename = 'profile_pics/'+current_user.profile_image)
    return render_template('account.html',form=form,profile_image=profile_image)


@users.route('/contact',methods=['GET','POST'])
def contact():
    form = AskForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = Message(f'From {name}', sender ='crypto.course.help@gmail.com',recipients=['crypto.course.help@gmail.com'])
        msg.body = f'Message is: \n {message} Email of sender is {email}'

        mail.send(msg)
        return redirect(url_for('core.index'))

    return render_template('contact.html',form=form)

@users.route('/forgot',methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user= User.query.filter_by(email=email).first()
        if user.confirmed:
            token = s.dumps(email, salt='password-change')
            msg = Message('Password change', sender ='crypto.course.help@gmail.com',recipients=[email])
            link = url_for('forgot_confirm',token=token,email=email,_external=True)
            msg.body = f'Your link is {link}'

            mail.send(msg)
            return f'The link was sent to your gmail {user.email}'
        else:
            return 'Sorry your account is not confirmed '
    return render_template('forgot.html',form=form)

@app.route('/forgot_confirm/<token>',methods=['GET', 'POST'])
def forgot_confirm(token):
    form = ChangePasswordForm()
    try:
       email = s.loads(token,salt='password-change',max_age=3600)
    except SignatureExpired:


        return 'The token is expired'


    if form.validate_on_submit():
        email = request.args.get('email', None)
        password = form.password.data
        user= User.query.filter_by(email=email).first()

        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('change.html',form=form,email=email)


admin.add_view(ModelView(User,db.session))
