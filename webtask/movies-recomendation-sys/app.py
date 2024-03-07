import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f1c50d8f1241b1f4520767a85a2e3696&language=en-US'.format(movie_id))
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path'].lstrip('/')  # Remove leading slash, if any
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Handle the case where there's no poster path
        return "https://via.placeholder.com/500x750"  # Placeholder image or any default image


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # enumerate function is used to hold the original position of index pointing to that movie even after sorting indexing doesn't loose

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id= movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('choose a movie you like',
                     movies['title'].values)

if st.button('Recommend'):
   names, posters = recommend(selected_movie_name)

   col1, col2, col3, col4, col5 = st.columns(5)
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



