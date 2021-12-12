from flask import Flask, render_template
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy 
from flask_user import login_required, UserManager, UserMixin
from flask_mail import Mail 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'swertemopagnahulaanmo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['CSRF_ENABLED'] = True 
app.config['USER_ENABLE_EMAIL'] = True 
app.config['USER_APP_NAME'] = 'AgriVance Pro'

app.config.from_pyfile('config.cfg')


db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column('confirmed_at', db.DateTime())


user_manager = UserManager(app, db, User)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True) 