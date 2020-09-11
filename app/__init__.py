from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s - %(funcName)s - %(message)s', filename='fr_handler.log')
logging = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from app import models
from app import views
db.create_all()

