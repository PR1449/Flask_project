import flask
from flask import request

from . import db_session
from .users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_jobs():
    db_sess = db_session.create_session()
    only = ['id', 'name', 'surname']
    jobs = db_sess.query(User).all()
    return flask.jsonify({
        'users': [item.to_dict(only=only) for item in jobs]
    })


@blueprint.route('/api/users/<int:users_id>')
def get_jobs_by_id(users_id):
    db_sess = db_session.create_session()
    only = ['id', 'name', 'surname', 'email']
    users = db_sess.query(User).filter(User.id == users_id).first()
    if not users:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify({
        'users': users.to_dict(only=only)
    })


@blueprint.route('/api/users', methods=['POST'])
def add_jobs():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    keys = ['id', 'name', 'surname', 'email']
    if not all([key in request.json for key in keys]):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == request.json['id']).first():
        return flask.jsonify({'error': 'ID already exists'})
    users = User()
    users.id = request.json['id']
    users.name = request.json['name']
    users.surname = request.json['surname']

    db_sess.add(users)
    db_sess.commit()
    return flask.jsonify({'success': 'ok'})
