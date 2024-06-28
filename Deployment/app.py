import streamlit as st
import requests
import pandas as pd
import hashlib
import pickle
import gdown
import os

# CSV files URLs as raw data from GitHub repository
moviesCSV = "https://raw.githubusercontent.com/Mohamed-Motaz-Mostafa/Movies-Recommender-System/main/Data/movies.csv?token=GHSAT0AAAAAACTODFY3DY4JKQVQFBL5RDV4ZT7KF5A" 
ratingsCSV = "https://raw.githubusercontent.com/Mohamed-Motaz-Mostafa/Movies-Recommender-System/main/Data/ratings.csv?token=GHSAT0AAAAAACTODFY2JIY6UAHMJ2V43HT6ZT7KGNA"
linksCSV = "https://raw.githubusercontent.com/Mohamed-Motaz-Mostafa/Movies-Recommender-System/main/Data/links.csv?token=GHSAT0AAAAAACTODFY2R32QAQGOTZTYIAHGZT7KG5Q"

# the folloing code is used to download the similarity matrix from google drive if not exist
file_url = 'https://drive.google.com/file/d/1-1bpusE96_Hh0rUxU7YmBo6RiwYLQGVy/view?usp=sharing'
output_path = 'Models/similarity_matrix.pkl'

@st.cache_data
def download_model_from_google_drive(file_url, output_path):
    gdown.download(file_url, output_path, quiet=False)
    

# # Check if the file already exists
if not os.path.exists(output_path):
    print("Downloading the similarity matrix from Googlr Drive...")
    download_model_from_google_drive(file_url, output_path)


# Set page configuration
st.set_page_config(page_title="Movie Recommendation", page_icon="🎬", layout="wide")

# Dummy data for user recommendations
user_recommendations = {
    "1": ["Inception", "The Matrix", "Interstellar"],
    "2": ["The Amazing Spider-Man", "District 9", "Titanic"]
}

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Dummy user database
user_db = {
    "1": hash_password("password123"),
    "2": hash_password("mypassword")
}

# Login function
def login(email, password):
    if email in user_db:
        return True
    return False

# Function to fetch movie details from OMDb API
def fetch_movie_details(title, api_key="23f109b2"):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Display movie details
def display_movie_details(movie):
    if movie['Response'] == 'False':
        st.write(f"Movie not found: {movie['Error']}")
        return
    if movie['imdbRating'] == 'N/A':
        movie['imdbRating'] = 0
    imdb_rating = float(movie['imdbRating'])
    url = f"https://www.imdb.com/title/{movie['imdbID']}/"
    st.markdown(
        f"""
        <div style="
            background-color: #313131;
            border-radius: 15px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex;">
                <div style="flex: 1;">
                <BR>
                    <a href="{url}" target="_blank" >
                    <img src="{movie['Poster']}" style="width: 100%; border-radius: 10px;" />
                    </a>
                </div>
                <div style="flex: 3; padding-left: 20px;">
                    <h2 style="margin: 0;" anchor="{url}">{movie['Title']}</h2>
                    <p style="color: gray;">
                        <b>Year:</b> {movie['Year']} Rated: {movie['Rated']} <br>
                        <b>Genre:</b> {movie['Genre'].replace(',',' |')} <br>
                    </p>
                    <p>{movie['Plot']}</p>
                    <div style="margin-top: 10px;">
                        <div style="background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
                            <div style="width: {imdb_rating * 10}%; background-color: #4caf50; padding: 5px 0; text-align: center; color: white;">
                                {imdb_rating}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )




def print_movie_details(movie):
    st.markdown(
        f"""
                                <div class="recommendation">
                                    <div style="display: flex;">
                                        <div style="flex: 1;">
                                         <a href="https://www.imdb.com/title/tt{movie['imdb_id']:07d}/" target="_blank">
                                            <img src="{movie['poster_url']}" />
                                            </a>
                                        </div>
                                        <div style="flex: 3; padding-left: 20px;">
                                            <h4 style="margin: 0;">{' '.join(movie['title'].split(" ")[:-1])}</h4>
                                            <p style="color: gray;">
                                                <b>Year:</b> {movie['title'].split(" ")[-1]}<br>
                                                <b>Genre:</b> {', '.join(movie['genres'])}<br>
                                                <b>Number of Ratings:</b> {movie['num_ratings']}<br>
                                                <b>IMDb Rating: </b>{round(movie["imdb_rating"],1)}<br>
                                            </p>
                                            <div style="margin-top: 10px;">
                                                <div style="background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
                                                    <div style="width: {movie['avg_rating'] * 20}%; background-color: #4caf50; padding: 5px 0; text-align: center; color: white;">
                                                        {movie['avg_rating']}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )



# Function to load data
@st.cache_data
def load_data():
    movies_df = pd.read_csv(moviesCSV)
    ratings_df = pd.read_csv(ratingsCSV)
    links_df = pd.read_csv(linksCSV)
    return movies_df, ratings_df, links_df

# Function to load similarity matrix
@st.cache_data
def load_similarity_matrix():
    with open('Models/similarity_matrix.pkl', 'rb') as f:
        similarity_df = pickle.load(f)
    return similarity_df

# Function to get movie details
def get_movie_details(movie_id, df_movies, df_ratings, df_links):
    try:
        imdb_id = df_links[df_links['movieId'] == movie_id]['imdbId'].values[0]
        tmdb_id = df_links[df_links['movieId'] == movie_id]['tmdbId'].values[0]

        movie_data = df_movies[df_movies['movieId'] == movie_id].iloc[0]
        genres = movie_data['genres'].split('|') if 'genres' in movie_data else []

        avg_rating = df_ratings[df_ratings['movieId'] == movie_id]['rating'].mean()
        num_ratings = df_ratings[df_ratings['movieId'] == movie_id].shape[0]

        api_key = 'b8c96e534866701532768a313b978c8b'
        response = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}' )
        poster_url = response.json().get('poster_path', '')
        full_poster_url = f'https://image.tmdb.org/t/p/w500{poster_url}' if poster_url else ''
        imdb_rating = response.json().get('vote_average', 0)

        return {
            "title": movie_data['title'],
            "genres": genres,
            "avg_rating": round(avg_rating, 2),
            "num_ratings": num_ratings,
            "imdb_id": imdb_id,
            "tmdb_id": tmdb_id,
            "poster_url": full_poster_url,
            "imdb_rating": imdb_rating  
        }
    except Exception as e:
        st.error(f"Error fetching details for movie ID {movie_id}: {e}")
        return None

# Function to recommend movies
def recommend(movie, similarity_df, movies_df, ratings_df, links_df, k=5):
    try:
        index = movies_df[movies_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity_df.iloc[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:k+1]:
            movie_id = movies_df.iloc[i[0]]['movieId']
            movie_details = get_movie_details(movie_id, movies_df, ratings_df, links_df)
            if movie_details:
                recommended_movies.append(movie_details)
        return recommended_movies
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

# Main app

def main():
    st.markdown(
        """
        <style>
        body {
            background-image: url("https://repository-images.githubusercontent.com/275336521/20d38e00-6634-11eb-9d1f-6a5232d0f84f");
            color: #FFFFFF;
            font-family: 'Arial', sans-serif;
        }

        .stApp {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 20px;
        }

        .title {
            font-size: 3em;
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
            color: #FF0000;
        }

        .section-title {
            font-size: 2em;
            margin-top: 30px;
            margin-bottom: 20px;
            text-align: center;
            color: #FFD700;
        }

        .recommendation {
            border: 1px solid #FFD700;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            background-color: rgba(0, 0, 0, 0.8);
            overflow: hidden;
        }

        .recommendation:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
        }

        .recommendation img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }

        .movie-details-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .movie-details-container .movie-poster {
            flex: 0 0 auto;
            width: 30%;
            margin-right: 20px;
        }

        .movie-details-container .movie-poster img {
            width: 100%;
            border-radius: 10px;
        }

        .movie-details-container .movie-details {
            flex: 1 1 auto;
        }

        .movie-details-container .movie-details p {
            margin: 5px 0;
        }

        a {
            color: #FFD700;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .stSidebar .element-container {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 15px;
        }

        .stSidebar .stButton button {
            background-color: #FFD700;
            color: #000;
            border: none;
            border-radius: 10px;
            padding: 10px;
            transition: background-color 0.2s, transform 0.2s;
        }

        .stSidebar .stButton button:hover {
            background-color: #FFAA00;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    movies_df, ratings_df, links_df = load_data()
    similarity_df = load_similarity_matrix()
    
    st.sidebar.title("Navigation")
    menu = ["Login", "Movie Similarity"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    if choice == "Login":
        st.title("Movie Recommendations")
        st.write("Welcome to the Movie Recommendation App!")
        st.write("Please login to get personalized movie recommendations. username between (1 and 800)")
        st.write("leve password blank for now.")
        
        # Login form
        st.sidebar.header("Login")
        email = st.sidebar.text_input("Username")
        # password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login(email, 'password'):
                st.sidebar.success("Login successful!")
                recommendations = user_recommendations.get(email, [])
                st.write(f"Recommendations for user number {email}:")
                num_cols = 2
                cols = st.columns(num_cols)
                for i, movie_title in enumerate(recommendations):
                    movie = fetch_movie_details(movie_title)
                    if movie['Response'] == 'True':
                        with cols[i % num_cols]:
                            display_movie_details(movie)
                    else:
                        st.write(f"Movie details for '{movie_title}' not found.")
            else:
                st.sidebar.error("Invalid email or password")

    elif choice == "Movie Similarity":
        num_cols = 2
        cols = st.columns(num_cols)
        
        # Movie similarity search
        with cols[0]:
            st.title("Find Similar Movies")
            selected_movie = st.selectbox("Type or select a movie from the dropdown", movies_df['title'].unique())
            k = st.slider("Select the number of recommendations (k)", min_value=1, max_value=50, value=5)
            button = st.button("Find Similar Movies")
        with cols[1]:
            st.title("Choosen Movie Details:")
            if selected_movie:
                correct_Name = selected_movie[:-7]
                movie = fetch_movie_details(correct_Name)
                if movie['Response'] == 'True':
                    display_movie_details(movie)
                else:
                    st.write(f"Movie details for '{selected_movie}' not found.")
        if button:
            st.write("The rating bar here is token from our dataset and it's between 0 and 5.")
            if selected_movie:
                recommendations = recommend(selected_movie, similarity_df, movies_df, ratings_df, links_df, k)
                if recommendations:
                    st.write(f"Similar movies to '{selected_movie}':")
                    num_cols = 2
                    cols = st.columns(num_cols)

                    # movie_id = movies_df[movies_df['title'] == selected_movie]['movieId'].values[0]
                    # movie_details = get_movie_details(movie_id, movies_df, ratings_df, links_df)
                    # if movie_details:
                    #     st.markdown(f'<h2 class="section-title">{movie_details["title"]} Details:</h2>', unsafe_allow_html=True)
                    #     st.markdown(
                    #         f"""
                    #         <div class="movie-details-container">
                    #             <div class="movie-poster">
                    #                 <img src="{movie_details['poster_url']}" alt="Movie Poster">
                    #             </div>
                    #             <div class="movie-details">
                    #                 <p><b>Genres:</b> {', '.join(movie_details['genres'])}</p>
                    #                 <p><b>Average Rating:</b> {movie_details['avg_rating']}</p>
                    #                 <p><b>Number of Ratings:</b> {movie_details['num_ratings']}</p>
                    #                 <p><b>IMDb :</b> <a href="https://www.imdb.com/title/tt{movie_details['imdb_id']:07d}/" target="_blank">movie link</a></p>
                    #             </div>
                    #         </div>
                    #         """,
                    #         unsafe_allow_html=True
                    #     )


                    
                    for i, movie in enumerate(recommendations):
                            with cols[i % num_cols]:
                                print_movie_details(movie)
                else:
                    st.write("No recommendations found.")
            else:
                st.write("Please select a movie.")

if __name__ == "__main__":
    main()
