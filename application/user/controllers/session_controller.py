from flask import request, Blueprint
from application.user.services.session_service import SessionService
from flask_socketio import SocketIO


def configure_session_views(app):
    sessions_bp = Blueprint('/sessions', __name__)

    @sessions_bp.route('/sessions/callback')
    def session_callback(session_service: SessionService, socket_io: SocketIO):
        client_id = request.args.get('state')
        code = request.args.get('code')
        request_info = (request.url, request.base_url)

        response = session_service.new_session(code, request_info)
        socket_io.emit(f"server::user::logged_in::{client_id}", response)

        return (
            '<script>window.close();</script>'
            '<p>Please close this tab</p>'
        )

    app.register_blueprint(sessions_bp)
