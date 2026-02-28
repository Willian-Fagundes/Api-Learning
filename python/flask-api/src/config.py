import os

class config:
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    JWT_SECRET_KEY = "secretKey"
    JWT_VERIFY_SUB = False