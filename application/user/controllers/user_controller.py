from flask import jsonify
from application.user.services.user_service import UserService
from flask.blueprints import Blueprint


def configure_user_views(app):
    users_bp = Blueprint('/users', __name__)

    @users_bp.route('/users', methods=['GET'])
    def get_users(user_service: UserService):
        users = user_service.get_all()
        return jsonify([u.serialize() for u in users])

    app.register_blueprint(users_bp)
