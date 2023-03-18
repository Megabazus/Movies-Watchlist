import json
import requests
import tmdbsimple as tmdb
import config
from flask import render_template
from datetime import date, datetime

print("S1_TMDB.py - Imports done, start code.")

# Required to add API KEY
tmdb.API_KEY = [config.API_KEY]
api_url = ["https://api.themoviedb.org/3"]

# Reformat current_date into YYmmdd
current_date = date.today()
current_date = current_date.strftime("%Y%m%d")


class Movie:
    def __init__(self, mid, title, original_language, popularity, release_date, overview):
        self.mid = mid
        self.title = title
        self.original_language = original_language
        self.popularity = popularity
        self.release_date = release_date
        self.overview = overview
        self.myRating = 0


testClass = []
x = Movie(123, "goz", "en", 8, '2022-01-01', 'hello')
testClass.extend([x.mid, x.title, x.original_language])


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


print("S2_TMDB.py - Load def trending_media")


def trending_media(media_type, time_window):
    try:
        check_file = open('data/daily_trending_movies_%s.json' % current_date)
        print("File Exists. Start loading process.")
        response_trending = json.load(check_file)
        check_file.close()
    except:
        print("File not available. Start API extract.")
        trending = tmdb.find.Trending(media_type=media_type, time_window=time_window)
        response_trending = trending.info()
        print(response_trending)
        with open("data/daily_trending_movies_%s.json" % current_date, "w") as write_file:
            json.dump(response_trending, write_file)

    # How to read results in the JSON output
    daily_trend_movies = []
    for movie in response_trending['results']:
        print(movie)
        daily_trend_movies.append(movie['title'])
        #print(movie['title'])
    print(daily_trend_movies)
    return daily_trend_movies


print(trending_media("movie", "day"))
print("S3_TMDB.py - Load def movie_search")


def movie_search(search):
    # Search TMDB for movies
    print("Start movie_search function.")
    searching = tmdb.Search()
    response_search = searching.movie(query=search)
    print(response_search)
    sorted_date = sorted(response_search['results'], key=lambda x: x['popularity'], reverse=True)
    movielist = []
    for movie in sorted_date: #response_search['results']:
        print(movie.get('id'),
              movie.get('title'),
              movie.get('original_language'),
              movie.get('popularity'),
              movie.get('release_date'),
              movie.get('overview'))
        movielist.append(Movie(movie.get('id'),
              movie.get('title'),
              movie.get('original_language'),
              movie.get('popularity'),
              movie.get('release_date'),
              movie.get('overview')))
        #movielist.append(movie['title'])
    return movielist

# Test the movie_search function
# print(movie_search("jurassic park"))

#Python get() method Vs dict[key] to Access Elements
# get() method returns a default value if the key is missing.
# However, if the key is not found when you use dict[key], KeyError exception is raised.

def db_duplicate_check(cursor,mid,lid):
    cursor.execute(
        "SELECT COUNT(*) FROM movies WHERE mid = %d and lid = %d" % (mid, lid))
    res = cursor.fetchone()
    return res[0] > 0

# Get movie information
def get_movie(mid):
    movie_url = api_url + \
        "movie/%s" % (mid) + "?language=en-US&api_key=%s" % (api_key)
    base_img_url = 'https://image.tmdb.org/t/p/w500'
    movie = get_json(movie_url)
    movie = Movie(movie.get('id'),
                  movie.get('title').replace('"', ''),
                  base_img_url + movie.get('poster_path'),
                  movie.get('popularity'),
                  movie.get('release_date').replace('"', ''),
                  movie.get('overview').replace('"', ''))
    return