from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dotenv import DotEnv

db = SQLAlchemy()
migrate = Migrate()  # Initializes Flask-Migrate

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    env = DotEnv()
    env.init_app(app)
    
    app.run(debug=True)
    # Configure app from config.py
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Binds the app and db to Flask-Migrate
    
      # Enable debug mode
    app.debug = True
    
    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
