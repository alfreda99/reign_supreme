from flask import Flask
from .static.components.home.routes import home

#https://exploreflask.com/en/latest/configuration.html

app = Flask(__name__)

# Load the environment specific configuration
app.config.from_object('config.development')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

app.register_blueprint(home)
