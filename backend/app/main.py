from fastapi import FastAPI

from app.services.naver import search_naver_blog
from app.services.tmdb import get_netflix_movies

app = FastAPI(title="OTT Situation Picker API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/contents")
def get_contents():
    return get_netflix_movies()


@app.get("/api/reviews")
def get_reviews(movie_title: str):
    return search_naver_blog(movie_title)


@app.get("/api/contents-with-reviews")
def get_contents_with_reviews():
    movies = get_netflix_movies()

    for movie in movies:
        movie["reviews"] = search_naver_blog(f"{movie['title']} 영화")

    return movies
