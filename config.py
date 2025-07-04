import os

class Config:
    SECRET_KEY = 'ABCDEabcde12345'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
