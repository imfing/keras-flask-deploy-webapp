from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from PIL import Image
import numpy as np

# Define a flask app
app = Flask(__name__)

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="import")
    return graph


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        image = Image.open(file_path)
        image = np.array(image)
        y_out = persistent_sess.run(y, feed_dict={
            x: image
        })

        prediction = np.argmax(y_out, 1)
        result = '%.2f_%.2f' % (y_out[0][0], y_out[0][1])
        return result, prediction
    return None


if __name__ == '__main__':
    print('Loading the model')
    graph = load_graph('./models/iasante_model.pb') #(args.frozen_model_filename)
    x = graph.get_tensor_by_name(u'import/Cast:0')
    y = graph.get_tensor_by_name(u'import/final_guess:0')
    # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory)
    # sess_config = tf.ConfigProto(gpu_options=gpu_options)
    # persistent_sess = tf.Session(graph=graph, config=sess_config)
    persistent_sess = tf.Session(graph=graph)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
