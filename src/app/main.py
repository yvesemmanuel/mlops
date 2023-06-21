from flask import (
    Flask,
    request,
    jsonify
)
from textblob import TextBlob
import pickle


app = Flask(__name__)
model = pickle.load(open('models/model.sav', 'rb'))


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/sentiment/<sentence>')
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
