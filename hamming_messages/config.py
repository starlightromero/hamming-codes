"""Import os and dotenv."""
import os
from dotenv import load_dotenv


class Config:
    """Config class."""

    ENV = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
