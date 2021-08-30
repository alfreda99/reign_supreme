from flask import Flask


app = Flask(__name__)

# Load the environment specific configuration
app.config.from_object('config.production')

from .static.components.home.routes import home

app.register_blueprint(home)

