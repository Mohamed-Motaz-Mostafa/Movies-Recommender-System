import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor


def train_model(data,user_id, test=None, eval = False):


    # select only user data
    train_user = data[data['userId']==user_id]


    X_train = train_user.drop(columns=['userId','rating', 'Train', 'title'])
    y_train = train_user['rating']

    model = XGBRegressor()
    model.fit(X_train,y_train)

    if eval:
        test_user = test[test['userId']== user_id]
        X_test = test_user.drop(columns=['userId','rating', 'Train', 'title'])
        y_test = test_user['rating']
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f'RMSE: {rmse:.4f}')
    # Model evaluation
    # print("Predected rating:", y_pred)
    # print("Actual rating:",y_test)
    # print(X_test)

    return model

def get_user_recommendation_XGBoost(all_moves,model, user_id, n=10):
    # get all movies that the user has not seen
    user_seen_movies = all_moves[all_moves['userId'] == user_id]['title']
    user_unseen_movies = all_moves[~all_moves['title'].isin(user_seen_movies)]

    # drop duplicates
    user_unseen_movies = user_unseen_movies.drop_duplicates(subset=['title'])

    # make predictions
    user_unseen_movies['Pred_rating'] = model.predict(user_unseen_movies.drop(columns=['userId', 'rating', 'Train', 'title']))

    # only return movies with more than 100 ratings

    # get top 10 recommendations
    recommendations = user_unseen_movies.sort_values(by='Pred_rating', ascending=False).head(n)['title']
    return recommendations ,user_seen_movies



def get_user_recommendation(DataBase, Matrix,user_id,l=10):
    user = Matrix[user_id]
    user = user.sort_values(ascending=False)
    # now we have a series of user similarities
    # we only want to recommend movies that the user has not seen
    # so we need to filter out movies that the user has seen
    user_seen_movies = DataBase[DataBase['userId'] == user_id]['title']


    # Now we loop through user and get top 10 recommendations
    recommendations = []
    print(len(user.index))
    for U in user.index[1:10]:
        # get all rated movies by user U
        movies = DataBase[DataBase['userId'] == U]['title']
        movies = movies[~movies.isin(user_seen_movies)]

        # get all movies that U has rated 4 or higher
        movies = movies[DataBase['rating'] >= 4]
        # sort by rating
        movies = movies.sort_values(ascending=False)
        for movie in movies[:4]:   
            if movie not in recommendations:
                recommendations.append(movie) 
        
        if len(recommendations) >= l:
            break


       
    return recommendations


def get_recommendation_item(dataBase,matrix, movie_name, n=10):
  similar_scores = matrix[movie_name]
  similar_scores = similar_scores.sort_values(ascending=False)
  
  # only return movies with more than 100 ratings
  similar_scores = similar_scores[similar_scores.index.isin(dataBase[dataBase['number_of_ratings'] > 100].index)][:n]
  return similar_scores


if __name__ == '__main__':
    import pickle

    def load_similarity_matrix(path):
        with open(path, 'rb') as f:
            similarity_df = pickle.load(f)
        return similarity_df

    # Load the data
    DataBaseCSV = r"D:\Study\ITI\Recommender Systems\Final\Movies-Recommender-System\Data\XGBoost_database.csv"
    DataBase = pd.read_csv(DataBaseCSV)
    # Load the similarity matrix
    MatrixCSV = r"D:\Study\ITI\Recommender Systems\Final\Movies-Recommender-System\Models\user_based_matrix.pkl"
    Matrix = load_similarity_matrix(MatrixCSV)   
    recommendations = get_user_recommendation(DataBase, Matrix,1)
    print(recommendations)

