from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost:3309/cs01saled?charset=utf8mb4' % quote('03112002')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'
app.config['PRODUCT_KEY'] = 'product'

cloudinary.config(cloud_name='dnjmavk9l', api_key='874861645267929', api_secret='88g0EdzzYJyJE4Wm8JSUvfWjU-I')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'