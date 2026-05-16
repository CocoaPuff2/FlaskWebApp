from flask import Flask
from flask_sqlalchemy import SQLAlchemy # use for database
from os import path 
from flask_login import LoginManager

db = SQLAlchemy() # use whenever add user to database 
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'iegjowigoweig'
    # tell flask where db is (location)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #initialize db 
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note # load the file before init db 

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # if db doesn't exist ,,create one, don't override it 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')