from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Import all routes
# These imports need to be at the bottom to avoid circular imports
from .main import *
from .instrument import * 