import flask
import flask_injector
import injector


class Test:
    def __init__(self, msg):
        self.msg = msg

    def test(self):
        return 'hello world ' + str(self.msg)


class AppProvidersModule(injector.Module):

    def configure(self, binder):
        binder.bind(
            Test,
            to=self.create,
            scope=flask_injector.request
        )

    @injector.inject
    def create(
        self,
        config: flask.Config,
    ) -> 'Test':
        return Test(config.get('test'))
