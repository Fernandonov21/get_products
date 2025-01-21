import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:12345@127.0.0.1/readdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
