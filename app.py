from flask import Flask
from views import views

app = Flask(__name__)
app.secret_key = 'very_secret_key'
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MAX_CONTENT_PATH']


if __name__ == '__main__':

   app.register_blueprint(views, url_prefix='/')
   app.run(debug = True)

