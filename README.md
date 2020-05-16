# Deploy Keras Model with Flask as Web App in 10 Minutes

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![](https://img.shields.io/badge/python-3.5%2B-green.svg)]()
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

A pretty and customizable web app to deploy your DL model with ease

<a href="https://www.buymeacoffee.com/fing" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee"></a>

## Getting Started in 10 Minutes

- Clone this repo 
- Install requirements
- Run the script
- Go to http://localhost:5000
- Done! :tada:

:point_down: Screenshot:

<p align="center">
  <img src="https://user-images.githubusercontent.com/5097752/71063354-8caa1d00-213a-11ea-86eb-879238887c1f.png" height="420px" alt="">
</p>

## New Features :fire:

- Enhanced, mobile-friendly UI
- Support image drag-and-drop
- Use vanilla JavaScript, HTML and CSS. Remove jQuery and Bootstrap
- Switch to TensorFlow 2.0 and [tf.keras](https://www.tensorflow.org/guide/keras) by default
- Upgrade Docker base image to Python 3 (it's 2020)

<p float="left">
  <img src="https://user-images.githubusercontent.com/5097752/71065048-61c1c800-213e-11ea-92f1-274cbe4734ba.png" height="330px" alt="">
  <img src="https://user-images.githubusercontent.com/5097752/71062921-aeef6b00-2139-11ea-8b23-6b9eb1e326ca.png" height="330px" alt="">
</p>

_If you need to use Python 2.x or TensorFlow 1.x, check out the [legacy](https://github.com/mtobeiyf/keras-flask-deploy-webapp/tree/legacy) snapshot_


------------------

## Run with Docker

With **[Docker](https://www.docker.com)**, you can quickly build and run the entire application in minutes :whale:

```shell
# 1. First, clone the repo
$ git clone https://github.com/mtobeiyf/keras-flask-deploy-webapp.git
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
$ git clone https://github.com/mtobeiyf/keras-flask-deploy-webapp.git
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


## Deployment

To deploy it for public use, you need to have a public **linux server**.

<details>
 <summary>Details</summary>
  
### Run the app

Run the script and hide it in background with `tmux` or `screen`.
```
$ python app.py
```

You can also use gunicorn instead of gevent
```
$ gunicorn -b 127.0.0.1:5000 app:app
```

More deployment options, check [here](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/)

### Set up Nginx

To redirect the traffic to your local app.
Configure your Nginx `.conf` file.

```
server {
  listen  80;

  client_max_body_size 20M;

  location / {
      proxy_pass http://127.0.0.1:5000;
  }
}
```

</details>

## Future Plan

- [ ] Support detection and segmentation models

## More Resources

[Building a simple Keras + deep learning REST API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
