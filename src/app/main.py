from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
basic_auth = BasicAuth(app)

model = pickle.load(open('../../models/model.sav', 'rb'))


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/sentiment/<sentence>')
@basic_auth.required
def get_sentiment(sentence: str):
    tb = TextBlob(sentence)
    polarity = tb.sentiment.polarity

    return f'polarity: {polarity}'


@app.route('/house_price', methods=['POST'])
def get_house_price():
    body = request.get_json()
    model_input = [body[key] for key in ['tamanho', 'ano', 'garagem']]

    price = model.predict([model_input])

    return jsonify(price=price[0])


app.run(debug=True, host='0.0.0.0')
