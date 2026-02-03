"""Lambda handler for FastAPI backend using Mangum."""
import os
import sys

# Add the app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mangum import Mangum
from app.main import app

# Mangum adapter for AWS Lambda
handler = Mangum(app, lifespan="off")
