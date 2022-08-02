import json
import os
import requests
import tmdbsimple as tmdb

# Required to add API KEY
tmdb.API_KEY = ["627484326ecfe112b731976b08fb3e20"]
api_url = ["https://api.themoviedb.org/3"]


class Movie:
    def __init__(self, mid, title, poster, popularity, release_date, overview):
        self.mid = mid
        self.title = title
        self.poster = poster
        self.popularity = popularity
        self.release_date = release_date
        self.overview = overview
        self.myRating = 0


def get_json(url):
    # '''Returns json text from a URL'''
    response = None
    try:
        return requests.get(url).json()
    finally:
        if response != None:
            response.close()


def watchlist_popular():
    top_movies = tmdb.get_trending(timeframe='day')
    # return str(top_movies)
    return render_template("watchlist_popular.html", top_movies=top_movies)

# search = tmdb.Search()
# response = search.movie(query='Bourne')
# print(response)

# Example of finding daily trend movies: https://github.com/celiao/tmdbsimple/blob/master/tmdbsimple/find.py
# Trending() is the Class
# info(media_type='', time_window='') is the definition


trending = tmdb.find.Trending(media_type="movie", time_window="day")
response_trending = trending.info()
print(response_trending)
with open("trending_movies.json", "w") as write_file:
    json.dump(response_trending, write_file)

# How to read results in the JSON output
for movie in response_trending['results']:
    print(movie)
    # print(movie['title'])
