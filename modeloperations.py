import librosa

from sklearn.preprocessing import LabelEncoder

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# from tensorflow.keras.models import load_model
import numpy as np
from keras.models import model_from_json
import os
import pandas as pd
import random
from base64 import b64decode
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from joblib import dump, load

config = tf.compat.v1.ConfigProto(
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
session = tf.compat.v1.Session(config=config)

tf.compat.v1.keras.backend.set_session(session)


def load_model():
    global model
    json_file = open('/Users/anacrisan/facultate/licenta/code/keras-flask-deploy-webapp/models/model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights("/Users/anacrisan/facultate/licenta/code/keras-flask-deploy-webapp/models/model.h5")
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

encoder = OneHotEncoder()
encoder = load('/Users/anacrisan/facultate/licenta/code/keras-flask-deploy-webapp/models/encoder.joblib')


# data augmentation functions
def noise(data):
    noise_amp = 0.035 * np.random.uniform() * np.amax(data)
    data = data + noise_amp * np.random.normal(size=data.shape[0])
    return data


def stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate)


def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)


# extract features
def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result = np.hstack((result, zcr))  # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft))  # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc))  # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))  # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel))  # stacking horizontally

    return result


def get_features(path):
    # duration and offset are used to take care of the no audio in start and the ending of each audio file
    data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
    res = extract_features(data, sample_rate)
    result = np.array(res)
    result = np.vstack((result, res))
    result = np.vstack((result, res))
    return result


def model_predict(vector):
    try:
        with session.as_default():
            with session.graph.as_default():
                load_model()
                print('Model loaded. Start serving...')
                model.summary()
                X = []
                for ele in vector:
                    X.append(ele)
                Features = pd.DataFrame(X)
                Features['labels'] = [0,0,0]
                X = Features.iloc[:, :-1].values
                scaler = load('/Users/anacrisan/facultate/licenta/code/keras-flask-deploy-webapp/models/std_scaler.bin')
                X = scaler.transform(X)
                X = np.expand_dims(X, axis=2)
                preds = model.predict(X)
                print('Prediction:', preds[0])
                return encoder.inverse_transform(preds)

    except Exception as ex:
        print(ex)

    return ['emotionless']


def extract_features_and_predict(path):
    # Construct relative path
    random_number = random.randint(00000, 99999)
    print("does tmp exist?")
    print(os.path.isdir('tmp'))
    filepath = './tmp/' + str(random_number) + '.wav'
    wav_file = open(filepath, "wb")
    decode_string = b64decode(path)
    wav_file.write(decode_string)

    # Extract Audio Features
    x = get_features(filepath)
    # Make prediction
    preds = model_predict(x)
    print('Predictions:',preds)
    # Remove temporary file
    os.remove(filepath)

    # Return JSON formatted Predictions
    # responseObject = {
    #     "result": preds,
    #     "errors": 'none'
    # }

    return preds
