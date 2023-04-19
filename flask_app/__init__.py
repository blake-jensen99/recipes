from flask import Flask

app = Flask(__name__)

DB = 'recipes_schema'

app.secret_key = "secret"