from WebApp import app
from flask import render_template, url_for, redirect, request, jsonify
from flask.logging import default_handler
import pickle
import numpy as np
import logging

prediction_text = ''
model = pickle.load(open('WebApp/mushroom_classifier.pkl', 'rb'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('Predictions.log')
logger.addHandler(file_handler)
logger.removeHandler(default_handler)

@app.route('/')
def default():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html', prediction_text = prediction_text)

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    variables = np.array(list(data.values())).reshape(1, -1)
    prediction = model.predict(variables)
    if prediction == 0:
        output = 'Poisonous'
    else:
        output = 'Edible'
    return jsonify(output)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.form.to_dict().values()
            variables = [str(x) for x in data]
            output = model.predict(np.array(variables).reshape(1, -1))
            if output == 0:
                prediction_text = 'The Mushroom is Poisonous'
            else:
                prediction_text = 'The Mushroom is Edible'
            logger.info('Input: {}\nOutput: {}\n\n'.format(variables, prediction_text))
        except ValueError:
            prediction_text = 'Some Value Error.'

    return render_template('home.html', prediction_text = prediction_text)
