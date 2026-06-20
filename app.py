import os
import joblib
import gdown
import requests
import streamlit as st

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Google Drive File ID
# -----------------------------
FILE_ID = "https://drive.google.com/file/d/1jUNkoHXW2IyMl_a3kV7hq6FrW1CM5_A-/view?usp=drivesdk"
SIMILARITY_FILE = "similarity.pkl"


# -----------------------------
# Download similarity.pkl only once
# -----------------------------
@st.cache_resource
def load_similarity():

    if not os.path.exists(SIMILARITY_FILE):

        url = f"https://drive.google.com/uc?id={FILE_ID}"

        with st.spinner("Downloading similarity matrix... (Only first time)"):
            gdown.download(url, SIMILARITY_FILE, quiet=False)

    return joblib.load(SIMILARITY_FILE)


# -----------------------------
# Load Data
# -----------------------------
similarity = load_similarity()
movies = joblib.load("movies.pkl")


# -----------------------------
# Poster Function
# -----------------------------
OMDB_API_KEY = "13d344ce"


def fetch_poster(movie_title):

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        if data.get("Response") == "True":

            poster = data.get("Poster")

            if poster != "N/A":
                return poster

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/300x450?text=Error"


# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        title = movies.iloc[i[0]].title

        recommended_movies.append(title)

        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):

        with col:

            st.image(poster)

            st.caption(name)