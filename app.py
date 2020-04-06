import flask
import flask_injector
import injector
import providers
from environment import load_env_vars
from config.configuration import ConfigurationModule

load_env_vars()

INJECTOR_DEFAULT_MODULES = dict(
    config=providers.AppProvidersModule(),
)


def _configure_dependency_injection(
        flask_app, injector_modules, custom_injector
) -> None:
    modules = dict(INJECTOR_DEFAULT_MODULES)

    if injector_modules:
        modules.update(injector_modules)

    flask_injector.FlaskInjector(
        app=flask_app,
        injector=custom_injector,
        modules=modules.values(),
    )


def create_app(
        *,
        custom_injector: injector.Injector = None,
        injector_modules=None,
):
    app = flask.Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'hello world'

    @injector.inject
    @app.route('/calculate')
    def calculate(config: ConfigurationModule):
        var = config.get_var('GOOGLE_CLIENT_ID')
        return var if var is not None else 'None'

    _configure_dependency_injection(
        app, injector_modules, custom_injector)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run()
