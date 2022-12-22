from WebApp import app

@app.route('/')
def home():
    return 'Welcome'