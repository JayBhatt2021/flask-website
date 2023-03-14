"""Contains the application factory."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initializes the SQLAlchemy extension
db = SQLAlchemy()


def create_app():
    """Ensures that an instance of the Flask application (app) is created and
    configured.

    :return: The Flask app.
    """

    # Creates the app and ensures that the configuration file(s)
    # is/are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    # Loads the appropriate Config environment from config.py
    app.config.from_object("config.DevelopmentConfig")

    # Initializes the app with the SQLAlchemy extension
    db.init_app(app)

    # Registers the blueprints to the app
    register_blueprints(app)

    # Setups the database and login manager
    setup_database_and_login_manager(app)

    return app


def register_blueprints(app):
    """Registers all app blueprints.

    :param app: the Flask app
    """

    # Imports the auth and site modules from the current package
    from . import auth, site

    # Registers the blueprints of the auth and site modules
    app.register_blueprint(auth.bp, url_prefix="/")
    app.register_blueprint(site.bp, url_prefix="/")


def setup_database_and_login_manager(app):
    """Creates the project database and login manager.

    :param app: the Flask app
    """

    # Imports the Note and User database models (these database models must
    # be imported before db.create_all() is called)
    from .models import Note, User

    # Creates the app context and database, respectively
    with app.app_context():
        db.create_all()

    # Points the LoginManager instance to the Login Page
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Finds the current user of the session.

        :param user_id: the User ID
        :return: The current user.
        """

        return User.query.get(int(user_id))
