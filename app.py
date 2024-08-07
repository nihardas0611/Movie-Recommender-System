import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    base_url = "https://api.themoviedb.org/3/movie/{}"

    url = base_url.format(movie_id)

    params = {
        "language": "en-US",
        "api_key": "388ebeb15339dbb70e4420fa7a9f8ddb"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return None
    else:
        st.error(f"Error fetching data from TMDb API. Status code: {response.status_code}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id#fetch poster of a movie
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

similarity=pickle.load(open('similarity.pkl','rb'))

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")
selected_movie_name = st.selectbox(
    'Enter A Movie Name',
    movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)

    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])