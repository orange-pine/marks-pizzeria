import os

class Config:

    PASSWORD = "aP!p$Mx"
    PASSWORD_MARK = "cp2zc3bA"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{PASSWORD}@localhost:3306/mark_pizza"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "aP!p$M"