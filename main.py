import flask
from flask import Flask, render_template, redirect, make_response

from flask import Flask, render_template, redirect, make_response
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired
from deep_translator import GoogleTranslator

from data.users_resources import UsersResourse, UsersListResource
from flask_restful import Api
import requests
from json2html import *
import json


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
APP_ID = "a2ea1e71"
APP_KEY = "ff4176a57ef2625c2405874cf1bb00cb"

login_manager = LoginManager()
login_manager.init_app(app)


def translation(to_translate):
    translated = GoogleTranslator(source='auto').translate(to_translate)
    return translated


def get_recipes(q):
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.request("GET", url).json()
    infoFromJson = response
    hws = json2html.convert(json=infoFromJson)
    return hws


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    search = StringField('Впишите ингредиенты', validators=[DataRequired()])
    submit = SubmitField('Найти')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm()
    try:
        q = translation(form.search().split()[-1][7:-2])
        if q != '':
            return get_recipes(q)
        return render_template("main.html", form=form)
    except:
        return render_template("main.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(flask.jsonify({'error': 'Bad request'}), 400)


def main():
    db_session.global_init("db/recipes_users.db")
    # app.register_blueprint(recipes_api.blueprint)
    # api.add_resource(somthing, '/api/somsing')

    app.run()


if __name__ == '__main__':
    main()
