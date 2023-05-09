# Deploy Keras Model with Flask as Web App in 10 Minutes

[![](https://img.shields.io/badge/python-3.9%2B-green.svg)]()
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

A minimal and customizable repo to deploy your image models as web app easily.

## Getting Started

- Quick run with Docker:
  ```bash
  docker run --rm -p 5000:5000 ghcr.io/imfing/keras-flask-deploy-webapp:latest
  ```
- Go to http://localhost:5000 and enjoy :tada:

Screenshot:

<p align="center">
  <img src="./docs/screenshot.avif" height="420px" alt="">
</p>

## New Features :fire:

- Enhanced, mobile-friendly UI
- Support image drag-and-drop
- Use vanilla JavaScript, HTML and CSS. No jQuery or Bootstrap
- Switch to TensorFlow 2.x and [tf.keras](https://www.tensorflow.org/guide/keras) by default
- Upgrade Docker base image to Python 3.11

<p float="left">
  <img src="https://user-images.githubusercontent.com/5097752/71065048-61c1c800-213e-11ea-92f1-274cbe4734ba.png" height="330px" alt="">
  <img src="https://user-images.githubusercontent.com/5097752/71062921-aeef6b00-2139-11ea-8b23-6b9eb1e326ca.png" height="330px" alt="">
</p>

------------------

## Run with Docker

#### Use prebuilt image

```
$ docker run --rm -p 5000:5000 ghcr.io/imfing/keras-flask-deploy-webapp:latest
```

#### Build locally

With **[Docker](https://www.docker.com)**, you can quickly build and run the entire application in minutes :whale:

```shell
# 1. First, clone the repo
$ git clone https://github.com/imfing/keras-flask-deploy-webapp.git
$ cd keras-flask-deploy-webapp

# 2. Build Docker image
$ docker build -t keras_flask_app .

# 3. Run!
$ docker run -it --rm -p 5000:5000 keras_flask_app
```

Open http://localhost:5000 and wait till the webpage is loaded.

## Local Installation

It's easy to install and run it on your computer.

```shell
# 1. First, clone the repo
$ git clone https://github.com/imfing/keras-flask-deploy-webapp.git
$ cd keras-flask-deploy-webapp

# 2. Install Python packages
$ pip install -r requirements.txt

# 3. Run!
$ python app.py
```

Open http://localhost:5000 and have fun. :smiley:

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/71064959-3c34be80-213e-11ea-8e13-91800ca2d345.gif" height="480px" alt="">
</p>

------------------

## Customization

It's also easy to customize and include your models in this app.

> **Note**
> Also consider [gradio](https://github.com/gradio-app/gradio) or [streamlit](https://github.com/streamlit/streamlit) to create complicated web apps for ML models.

<details>
 <summary>Details</summary>

### Use your own model

Place your trained `.h5` file saved by `model.save()` under models directory.

Check the [commented code](https://github.com/mtobeiyf/keras-flask-deploy-webapp/blob/master/app.py#L37) in app.py.

### Use other pre-trained model

See [Keras applications](https://keras.io/applications/) for more available models such as DenseNet, MobilNet, NASNet, etc.

Check [this section](https://github.com/mtobeiyf/keras-flask-deploy-webapp/blob/master/app.py#L26) in app.py.

### UI Modification

Modify files in `templates` and `static` directory.

`index.html` for the UI and `main.js` for all the behaviors.

</details>

## More Resources

[Building a simple Keras + deep learning REST API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
