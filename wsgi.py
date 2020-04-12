from application import create_app
from application.socketio import socket_io
import ssl
import os
from werkzeug import run_simple
import logging

default_port = 5000
host = '0.0.0.0'

app = create_app()
if __name__ == '__main__':
    is_development = app.config.get('DEVELOPMENT')
    if is_development:
        logging.basicConfig(level=logging.DEBUG)
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_cert_chain('localhost.crt', 'localhost.key')
        run_simple(host, default_port, app, ssl_context=ctx)
        socket_io.run(app)
    else:
        port = int(os.environ.get('PORT', default_port))
        app.run(host=host, port=port)
