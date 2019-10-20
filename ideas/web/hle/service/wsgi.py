from flask import Flask

with open("flag.txt") as f:
    FLAG = f.read()

with open("secret.txt") as f:
    SECRET = f.read()

ADMIN_LOGIN = "admin"

app = Flask(__name__)

from .views import *
