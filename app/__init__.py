from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.trim_blocks = True
app.jinja_env.ltrim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.strip_blocks = True

bootstrap = Bootstrap(app)

from app import routes
