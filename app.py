import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import decode_predictions, preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


# Declare a flask app
app = Flask(__name__)
# Limit max upload size to 16MB to prevent DoS attacks
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Whitelist of allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    # Check if the file extension is in the allowed list
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# You can use pretrained model from Keras
# Check https://keras.io/applications/
# or https://www.tensorflow.org/api_docs/python/tf/keras/applications

# from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
# model = MobileNetV2(weights='imagenet')
# instead of MobileNetV2, use ResNet50V2 [change 1], Now EfficientNetB0 [change 2]
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input as efficientnet_preprocess
model = EfficientNetB0(weights='imagenet')

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'models/your_model.h5'

# Load your own trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')


def model_predict(img, model):
    print(model.input_shape)
    width, height = model.input_shape[1], model.input_shape[2]
    img = img.resize((width, height))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    
    # x = preprocess_input(x, mode='tf') #-> [change 2]
    x = efficientnet_preprocess(x)
    
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        #img = base64_to_pil(request.json)
        # Validate that JSON data exists in the request
        if not request.json:
            return jsonify(error="No input data provided"), 400

        # Extract base64 string from JSON
        img_base64 = request.json

        # Validate it is a string
        if not isinstance(img_base64, str):
            return jsonify(error="Invalid input format"), 400

        # Validate file type from base64 header
        ALLOWED_MIME_TYPES = ['data:image/png', 'data:image/jpeg',
                       'data:image/gif', 'data:image/webp']
        if not any(img_base64.startswith(mime) for mime in ALLOWED_MIME_TYPES):
            return jsonify(error="Invalid file type. Only PNG, JPEG, GIF, WEBP allowed"), 400

        # Attempt to convert base64 string to PIL image
        try:
            img = base64_to_pil(img_base64)
        except Exception:
            return jsonify(error="Invalid image format"), 400

        # Validate image is not None
        if img is None:
            return jsonify(error="Could not process image"), 400



        
        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        # preds = model_predict(img, model)
        try:
            preds = model_predict(img, model)
        except Exception:
            return jsonify(error="Prediction failed"), 500
        



        # Process your result for human
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability

        # This line was missing. It converts model numbers to Top-3 readable labels.
        pred_classes = decode_predictions(preds, top=3)
        
        #Format the Top-3 results into a readable string
        formatted_results = []
        for i in range(3):
            # Extract the label, replace underscores with spaces, and capitalize
            label = pred_classes[0][i][1].replace('_', ' ').capitalize()
            # Convert probability to a percentage string (e.g., 85.2%)
            score = "{:.1f}%".format(pred_classes[0][i][2] * 100)
            formatted_results.append(f"{label} ({score})")

        # Join all results into a single string separated by commas
        result = ", ".join(formatted_results)
        
        # Send the processed result and probability back to the frontend
        return jsonify(result=result, probability=pred_proba)

    return None

# Handle file size exceeded error
@app.errorhandler(413)
def too_large(e):
    return jsonify(error="File too large. Maximum size is 16MB"), 413
    
if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
