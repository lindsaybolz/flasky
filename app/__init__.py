from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Create access to db operations
db = SQLAlchemy()
migrate = Migrate()

# Load values from .env
load_dotenv()

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    # Set up DB
    if not test_config:
        # development environment config
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        # test environment config
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # connect the db and migrate to app
    db.init_app(app)
    migrate.init_app(app, db)

    # register routes
    from .routes import crystal_bp
    app.register_blueprint(crystal_bp)

    # import models
    from app.models.crystal import Crystal

    return app