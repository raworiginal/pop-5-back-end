import requests
import os
from dotenv import load_dotenv

load_dotenv()

from flask import Blueprint


api_bp = Blueprint("api_bp", __name__)

access_token = os.getenv("TMDB_ACCESS_TOKEN")
print(access_token)
