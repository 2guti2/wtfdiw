from application import create_app
import ssl
from werkzeug import run_simple

global heroku_app

if __name__ == '__main__':
    app = create_app()
    is_development = app.config.get('DEVELOPMENT')
    if is_development:
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_cert_chain('localhost.crt', 'localhost.key')
        run_simple('0.0.0.0', 5000, app, ssl_context=ctx)
    else:
        heroku_app = app
        heroku_app.run()
