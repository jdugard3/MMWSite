"""
This module initializes the API package.
It re-exports key components from the models and routes packages.
"""

# Import database instance
from api.models import db

# Import routes
from api.routes import api
