from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import journal_app, db
from app.models import User, Post



manager = Manager(journal_app)
migrate = Migrate(journal_app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
