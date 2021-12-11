from flask import Flask, render_template, url_for, request, session, flash, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
 
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
global COOKIE_TIME_OUT
#COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5 #5 minutes
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "caircocoders-ednalan-2020"
 
db = SQLAlchemy(app)
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    fullname = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  
    def __repr__(self):
        return '<user>'.format(self.username)
   
@app.route('/')
def index():
 if 'email' in session:
  username_session = session['email']
  user_rs = User.query.filter_by(email=username_session).first()
  return render_template('index.html', user_rs=user_rs)
 else:
  return redirect('/login')
 
@app.route('/login')
def login():
    passwordhash = generate_password_hash('test2')
    print(passwordhash)
    return render_template('login.html')
   
@app.route('/submit', methods=['POST'])
def login_submit():
 _email = request.form['inputEmail']
 _password = request.form['inputPassword']
 _remember = request.form.getlist('inputRemember')
  
 if 'email' in request.cookies:
  username = request.cookies.get('email')
  password = request.cookies.get('pwd') 
  row = User.query.filter_by(email=username).first()
  if row and check_password_hash(row.password_hash, password):
   #print(username + ' ' + password)
   session['email'] = row.email
   return redirect('/')
  else:
   return redirect('/login')
 # validate the received values
 elif _email and _password:
  #check user exists   
  row = User.query.filter_by(email=_email).first()  
  if row:
   if check_password_hash(row.password_hash, _password):
    session['email'] = row.email
    if _remember:
     resp = make_response(redirect('/'))
     resp.set_cookie('email', _email, max_age=COOKIE_TIME_OUT)
     resp.set_cookie('pwd', _password, max_age=COOKIE_TIME_OUT)
     resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
     return resp
    return redirect('/')
   else:
    flash('Invalid Password!')
    return redirect('/login')
  else:
   flash('Invalid Email Or Password!')
   return redirect('/login')   
   
 else:
  flash('Invalid Email Or Password!')
  return redirect('/login')
   
   
@app.route('/logout')
def logout():
 if 'email' in session:
  session.pop('email', None)
 return redirect('/')
  
if __name__ == '__main__':
 app.run(debug=True)
