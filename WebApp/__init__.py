from flask import Flask

app = Flask(__name__)
app.config['SECRET KEY'] = 'mushroom'

from WebApp import routes