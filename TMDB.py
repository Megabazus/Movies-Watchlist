import json
import requests
import tmdbsimple as tmdb
import config
import os
from datetime import date

# Required to add API KEY
from flask import render_template

tmdb.API_KEY = [config.API_KEY]
api_url = ["https://api.themoviedb.org/3"]
current_date = date.today()

# Reformat current_date into YYmmdd
current_date = current_date.strftime("%Y%m%d")

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


try:
    check_file = open('data/daily_trending_movies_%s.json' % current_date)
    print("File Exists. Start loading process.")
    response_trending = json.load(check_file)
except:
    print("File not available. Start API extract.")
    trending = tmdb.find.Trending(media_type="movie", time_window="day")
    response_trending = trending.info()
    print(response_trending)
    with open("data/daily_trending_movies_%s.json" % current_date, "w") as write_file:
        json.dump(response_trending, write_file)

# How to read results in the JSON output
daily_trend_movies = []
for movie in response_trending['results']:
    print(movie)
    daily_trend_movies.append(movie['title'])
    # print(movie['title'])
print(daily_trend_movies)

# Search TMDB for movies
searching = tmdb.Search()
response_search = searching.movie(query="Jurassic Park")
print(response_search)
