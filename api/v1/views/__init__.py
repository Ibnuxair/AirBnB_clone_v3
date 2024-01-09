from flask import Blueprint

# Create a Blueprint instance for versioned API views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing everything from index.py (wildcard import)
from .index import *
from .states import *
from .cities import *
from .amenities import *
