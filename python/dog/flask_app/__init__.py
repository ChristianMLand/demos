from flask import Flask

app = Flask(__name__)
app.secret_key = "itsasecret"
db = "dogs_db"