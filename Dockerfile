FROM ubuntu:16.04

# Install Python.
RUN \
    apt-get update && \
    apt-get install -y python python-dev python-pip python-virtualenv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR app

# reqs from file, to speed up dev iteration
RUN pip install Werkzeug Flask numpy Keras gevent pillow h5py tensorflow

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" , "app.py"]