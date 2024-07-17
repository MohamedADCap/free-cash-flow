import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    if DB_TYPE == 'postgres':
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
            f"{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
