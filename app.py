from flask import Flask, render_template, render_template, request, jsonify
from flask_user import login_required, UserManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_mail import Mail
import pickle
import sys
import os

app = Flask(__name__)

model = pickle.load(open(os.path.join('model', 'model.pkl'), 'rb'))

app.config['SECRET_KEY'] = 'bQeThWmZq4t6w9z$C&F)J@NcRfUjXn2r'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
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


@app.route('/prediction')
@login_required
def prediction():
    return render_template('prediction.html')


@app.route('/predict', methods=['POST'])
def predict():
    if current_user.is_authenticated:
        NSIC_RC_222 = float(request.get_json().get('NSIC_RC_222'))
        NSIC_RC_192 = float(request.get_json().get('NSIC_RC_192'))
        NSIC_RC_11 = float(request.get_json().get('NSIC_RC_11'))
        NSIC_RC_120 = float(request.get_json().get('NSIC_RC_120'))
        NSIC_RC_396 = float(request.get_json().get('NSIC_RC_396'))
        NSIC_RC_350 = float(request.get_json().get('NSIC_RC_350'))
        NSIC_RC_410 = float(request.get_json().get('NSIC_RC_410'))
        NSIC_RC_100 = float(request.get_json().get('NSIC_RC_100'))
        NSIC_RC_102 = float(request.get_json().get('NSIC_RC_102'))
        NSIC_RC_242 = float(request.get_json().get('NSIC_RC_242'))
        NSIC_RC_56 = float(request.get_json().get('NSIC_RC_56'))
        NSIC_RC_12 = float(request.get_json().get('NSIC_RC_12'))
        NSIC_RC_42 = float(request.get_json().get('NSIC_RC_42'))
        NSIC_RC_442 = float(request.get_json().get('NSIC_RC_442'))
        NSIC_RC_510 = float(request.get_json().get('NSIC_RC_510'))
        land_area = float(request.get_json().get('land_area'))
        seed_quantity = float(request.get_json().get('seed_quantity'))
        rainfall = float(request.get_json().get('rainfall'))
        maximum_temp = float(request.get_json().get('maximum_temp'))
        humidity = float(request.get_json().get('humidity'))

        # Predict yield based from X features
        X = [
            [
                NSIC_RC_222,
                NSIC_RC_192,
                NSIC_RC_11,
                NSIC_RC_120,
                NSIC_RC_396,
                NSIC_RC_350,
                NSIC_RC_410,
                NSIC_RC_100,
                NSIC_RC_102,
                NSIC_RC_242,
                NSIC_RC_56,
                NSIC_RC_12,
                NSIC_RC_42,
                NSIC_RC_442,
                NSIC_RC_510,
                land_area,
                rainfall,
                maximum_temp,
                humidity,
                seed_quantity,
            ]
        ]
        predicted_value = model.predict(X)

        return jsonify(data=predicted_value[0])
    else:
        return jsonify(redirect='/user/sign-in?next=/prediction')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
