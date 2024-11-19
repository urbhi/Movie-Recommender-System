import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c9a932353ef57ed5f45fa8c1613f70fc&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Moviesflix')
movies = pd.read_pickle(open("C:/Users/Lenovo/OneDrive/Desktop/streamlit/movie_recommender_endtoend/movies_name.sav","rb"))
similarity = pd.read_pickle(open("C:/Users/Lenovo/OneDrive/Desktop/streamlit/movie_recommender_endtoend/similarity.sav","rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    columns = st.columns(5)
    for i, column in enumerate(columns):
        column.text(recommended_movie_names[i])
        column.image(recommended_movie_posters[i])
 