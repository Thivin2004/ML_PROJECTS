import streamlit as st
import requests
import pickle

movies = pickle.load(open("E:\\ML_PROJECTS\\Movie_Recommendation_System\\movies_list.pkl", 'rb'))
similarity = pickle.load(open("E:\\ML_PROJECTS\\Movie_Recommendation_System\\similarity.pkl", 'rb'))

@st.cache_data
def fetch_poster(title):
    url = f"https://www.omdbapi.com/?t={title}&apikey=f8b88883"
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster'], data.get('Year', 'N/A'), data.get('imdbRating', 'N/A')
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster", 'N/A', 'N/A'

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    recommended_posters = []
    recommended_years = []
    recommended_ratings = []
    
    for i in distances[1:6]:  # Top 5
        movie_title = movies.iloc[i[0]].title
        poster_url, year, rating = fetch_poster(movie_title)
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)
        recommended_years.append(year)
        recommended_ratings.append(rating)
    
    return recommended_movies, recommended_posters, recommended_years, recommended_ratings

st.title("🎬 Movie Recommendation System")
st.markdown("Get similar movies recommendations instantly with posters, release year and ratings!")

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)


if st.button("Show Recommendations"):
    with st.spinner('Fetching Recommendations...'):
        names, posters, years, ratings = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
         st.image(posters[idx], use_container_width=True)  
         st.caption(f"**{names[idx]}**")
         st.text(f"Year: {years[idx]}")
         st.text(f"Rating: {ratings[idx]}/10")

