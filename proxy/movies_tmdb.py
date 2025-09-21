import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

BASE_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w185"
BASE_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
headers = {"accept": "application/json", "Authorization": f"Bearer {ACCESS_TOKEN}"}


def get_movie_by_id(movie_id):

    keys_to_keep = ["title", "overview", "release_date", "poster_path", "genres"]
    response = requests.get(BASE_DETAILS_URL + movie_id, headers=headers).json()
    response = {key: response[key] for key in keys_to_keep if key in response}

    response["poster_path"] = BASE_IMAGE_URL + response["poster_path"]
    response["genres"] = [genre["name"] for genre in response["genres"]]

    return response


def search_for_movie(params):
    keys_to_keep = ["id", "title", "poster_path", "release_date"]
    response = requests.get(BASE_SEARCH_URL, params=params, headers=headers).json()
    results = response["results"][:5]
    trimmed_results = []
    for result in results:
        result = {key: result[key] for key in keys_to_keep if key in result}
        if result["poster_path"]:
            result["poster_path"] = BASE_IMAGE_URL + result["poster_path"]
        trimmed_results.append(result)
    return trimmed_results


if __name__ == "__main__":
    params = {"query": "fast and furious"}

    test = search_for_movie(params)
    # test = get_movie_by_id("18")
    print(test)
