from application import create_app
from flask_migrate import MigrateCommand, Manager

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)

# make sqlalchemy detect the models
from application.user import user_model, session_model

if __name__ == '__main__':
    manager.run()
