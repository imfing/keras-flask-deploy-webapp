import os

from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect


from modeloperations import extract_features_and_predict
from base64 import b64encode
from rq import Queue
from worker import conn


q = Queue(connection=conn)
# Declare a flask app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['audio_file']
        enc = b64encode(file.read())

        preds = extract_features_and_predict(enc)

        result = preds[0].tolist()
        print(result)
        res = jsonify(emotion=result)
        return res

    return None


if __name__ == '__main__':
    portnum = int(os.environ.get("PORT", 5432))
    app.run(host='0.0.0.0', port=portnum, threaded=True)
