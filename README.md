# 🎬 Movie Recommendation System 🎬

🎬 Looking for the perfect movie to watch this weekend? 🎬

Check out our [Movie Recommendation System](https://lnkd.in/dNhwjm9f) on Hugging Face.

## 📖 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Team](#team)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## 🎥 Introduction

This project provides a robust movie recommendation system that helps users discover similar movies and get personalized recommendations based on their viewing history. By leveraging advanced algorithms and machine learning techniques, this system aims to enhance the movie-watching experience.

## ⭐ Features

### 1. Discover Similar Movies
Use the Item-Based Similarity page to select a movie you enjoyed and find similar titles that you may love.

### 2. Personalized Recommendations
Visit the User-Based Similarity page, log in as a random user (1 to 609), and see recommendations tailored to user history.

## 💻 Technologies Used

### 1. Similarity Matrix
Algorithms to compare movies based on various features and identify similar movies that align with your tastes.

### 2. XGBoost
A powerful gradient-boosting framework that enhances recommendations for each user by analyzing user history to predict preferences.

### 3. API Integration
Leverages external movie databases for comprehensive details, including ratings, genres, and summaries to enrich the user experience.

## 🛠️ Installation

To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Mohamed-Motaz-Mostafa/Movies-Recommender-System.git
   ```
2. Navigate to the project directory:
```bash
cd Movies-Recommender-System
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

# 🚀 Usage
## Running the App
Download CSV Data from GitHub:
Ensure you have access to the CSV data stored in the GitHub repository.

## Load the Model:
The model can be downloaded from Google Drive using a direct download link. Here's an example code snippet to load the model:
```python
import requests
import pickle

def load_model_from_gdrive(gdrive_url):
    response = requests.get(gdrive_url)
    model = pickle.loads(response.content)
    return model

gdrive_model_url = 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID'
similarity_df = load_model_from_gdrive(gdrive_model_url)
```
## Start the Streamlit App:

```bash
streamlit run app.py
```
## Interacting with the App
Item-Based Similarity Page:
Select a movie to find similar titles.<br>
User-Based Similarity Page:
Log in as a random user to see personalized recommendations.<br>
# 👥 Team
Mohamed Motaz <br>
Amina Mohamed <br>
Asmaa Ali <br>
Naira Mohamed <br>
Shorouq Hossam <br>
