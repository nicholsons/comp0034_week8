from pathlib import Path

import pandas as pd
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
# login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_classname):
    """
    Initialise and configure the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    db.init_app(app)
    # login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from my_app.models import User, LocalAuthority
        db.create_all()
        # Uncomment the following if you want to experiment with reflection
        # db.Model.metadata.reflect(bind=db.engine)

        # Add the local authority data to the database (this is a workaround you don't need this for your coursework!)
        csv_file = Path(__file__).parent.parent.joinpath("data/household_recycling.csv")
        la_data = pd.read_csv(csv_file, usecols=['Code', 'Area'])
        la_data.drop_duplicates(inplace=True)
        # la_data.sort_values(by=['Area'], inplace=True)
        la_data.to_sql('local_authority', db.engine, if_exists='replace')

        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    from my_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
