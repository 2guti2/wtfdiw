from application import create_app
import ssl
import os
from werkzeug import run_simple

app = create_app()
if __name__ == '__main__':
    is_development = app.config.get('DEVELOPMENT')
    if is_development:
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_cert_chain('localhost.crt', 'localhost.key')
        run_simple('0.0.0.0', 5000, app, ssl_context=ctx)
    else:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
