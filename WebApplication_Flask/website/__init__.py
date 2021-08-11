from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db= SQLAlchemy() # Define a new database
DB_NAME= "database.db"

def create_app():
    app = Flask(__name__) #initialize the flask app
    app.config['SECRET_KEY'] = 'You-will-Never-Know' # We will use the config variable to apply a Secret Key to encrypt our cookies and data
    # We will use SQLITE Database
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}' # This will store the database into the website folder and will tell Flask it's location
    db.init_app(app) # Initialize the database

    # Import the blueprints
    from .views import views
    from .auth import auth
    # We need to register the blueprints to our application
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note # To make sure that the models.py file works before we initialize our database

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Location to go when we are not logged in i.e. auth.login
    login_manager.init_app(app)  # telling login manager which app we are using
    #Now we need to tell flask how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    """
    Check if the dat5abase exist else it will create a new database
    :param app:
    :return: None
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
