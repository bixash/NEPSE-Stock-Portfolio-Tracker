from flask import Flask
from .views import views
from .auth import auth


def create_app():
    app = Flask(__name__)
    app.secret_key = 'very_secret_key'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app