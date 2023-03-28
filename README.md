# Deploying Brain Tumor Keras Pre-Trained Model with Flask as Web App

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![](https://img.shields.io/badge/python-3.5%2B-green.svg)]()
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)


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

## Installation


```shell
# 1. First, clone the repo
$ git clone https://github.com/HameemDakheel/brain-tumors-classification-webapp.git
$ cd brain-tumors-classification-webapp

# 2. Install Python packages
$ pip install -r requirements.txt

# 3. Run!
$ python app.py
```

Open http://localhost:5000 and have fun. :smiley:


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


## More Resources

[Building a simple Keras + deep learning REST API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)


## Authors

* **Xin** - *Initial work* - [imfing](https://github.com/imfing)

See also the [original project](https://github.com/imfing/keras-flask-deploy-webapp).