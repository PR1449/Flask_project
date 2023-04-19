from flask_restful import Resource, reqparse, abort, Api
from . import db_session
from .users import User
from .parser import parser
from flask import jsonify


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} is not found")


class UsersResourse(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        only = ['id', 'surname', 'name', 'email', 'hashed_password']
        return jsonify({'user': user.to_dict(only=only)})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()

        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        only = ['id', 'surname', 'name', 'email', 'hashed_password']
        return jsonify({'users': [user.to_dict(only=only) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = User()
        user.id = args['id']
        user.surname = args['surname']
        user.name = args['name']
        user.email = args['email']
        user.hashed_password = args['hashed_password']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
