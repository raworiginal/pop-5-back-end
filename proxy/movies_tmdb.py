import os
import requests
import json
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

BASE_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w185"

headers = {"accept": "application/json", "Authorization": f"Bearer {ACCESS_TOKEN}"}


def get_movie_by_id(movie_id):

    response = requests.get(BASE_DETAILS_URL + movie_id, headers=headers).json()
    keys_to_keep = ["title", "overview", "release_date", "poster_path", "genres"]
    response = {key: response[key] for key in keys_to_keep if key in response}

    response["poster_path"] = BASE_IMAGE_URL + response["poster_path"]
    response["genres"] = [genre["name"] for genre in response["genres"]]

    return response


if __name__ == "__main__":
    test = get_movie_by_id("18")
    print(test)
