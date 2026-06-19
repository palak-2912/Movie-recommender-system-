import streamlit as st
import pickle
import requests


url = "https://drive.google.com/file/d/1jUNkoHXW2IyMl_a3kV7hq6FrW1CM5_A-/view?usp=drive_link/similarity.pkl"
response = requests.get(url)
with open("similarity.pkl", "wb") as f:
    f.write(response.content)

similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_title):
    api_key = "13d344ce"   # your OMDB API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=13d344ce"

    try:
        response = requests.get(url, timeout=8)
        data = response.json()

        poster_url = data.get("Poster")

        if poster_url and poster_url != "N/A":
            return poster_url
        else:
            # fallback placeholder
            return "https://via.placeholder.com/300x450?text=No+Image"

    except Exception:
        # fallback placeholder on error
        return "https://via.placeholder.com/300x450?text=Error"




st.title("Movie Recommender System")

# Load movie data
movies = pickle.load(open("movies.pkl", "rb"))
movies_list = movies["title"].values

# Load similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters



# Dropdown box
selected_movie = st.selectbox("Select a movie", movies_list)

# Button
if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
