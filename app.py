import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=d9c4f8389e340b5e09bed2e2bba3d603&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]

    recommendations = np.argsort(-distances)[:10]
    recommended_movies = []
    for i in recommendations:
        recommended_movies.append([movies.iloc[i].title, movies.iloc[i].movie_id])
    return recommended_movies

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select Movie You Would Like To Watch",
    movies['title'],
)

# st.button("Reset", type="primary")
if st.button("Recommend"):
    recommended_movies = recommend(selected_movie_name)

    cols = st.columns(3)
    i = 0

    for movie in recommended_movies:
        with cols[i%3]:
            st.subheader(movie[0])
            st.image(fetch_poster(movie[1]))
        i +=1
