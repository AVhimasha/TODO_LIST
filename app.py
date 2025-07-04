from flask import Flask
from flask_login import LoginManager
from config import Config
from model import db, User
from auth_routers import auth
from task_routers import task
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.init_app(app)

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(task)

# Create DB
db_created = False

@app.before_request
def create_tables():
    global db_created
    if not db_created:
        db.create_all()
        db_created = True

# To initialize migrations, run in terminal:
# flask db init
# To generate a migration after model changes:
# flask db migrate -m "message"
# To apply migrations:
# flask db upgrade

if __name__ == '__main__':
    app.run(debug=True)
