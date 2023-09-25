from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Email

def email_contains_at_the_rate_field(form, field):
    if "@" not in field.data: 
        raise ValidationError(message=f"Please include an '@' in the email address. '{field.data}' is missing an '@'." )

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your Uoft Email address?', validators=[email_contains_at_the_rate_field])
    is_utoronto = HiddenField()
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KlienMoretti876*'
moment = Moment(app)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        is_utoronto = session.get('is_utoronto')
        if old_name is not None and old_name != form.name.data.split()[0]:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data.split()[0]
        session['email'] = form.email.data
        if "utoronto" not in session['email']:
            is_utoronto = False
        else:
            is_utoronto = True
        session['is_utoronto'] = is_utoronto
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), is_utoronto=session.get('is_utoronto'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())