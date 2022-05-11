import boto3
import pandas as pd
import MoreLikeX

items_df = pd.read_csv('C:/Users/Andzej/Desktop/ml-latest-small/movies.csv')
items_df.sample(10)
users_data_df = pd.read_csv('./users.csv')
personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')
recommender_top_picks_arn = 'arn:aws:personalize:us-east-1:217528143255:recommender/top_picks_for_you'


def get_gender_by_id(user_id, user_df):
    return user_df.loc[user_df["USER_ID"] == int(user_id)]['GENDER'].values[0]
    try:
        return user_df.loc[user_df["USER_ID"] == int(user_id)]['GENDER'].values[0]
    except:
        print(user_id)
        return "Error obtaining title"


def get_movie_by_id(movie_id, movie_df):
    try:
        return movie_df.loc[movie_df["movieId"] == int(movie_id)]['title'].values[0]
    except:
        print(movie_id)
        return "Error obtaining title"


# First pick a user
test_user_id = "1"

# Get recommendations for the user
get_recommendations_response = personalize_runtime.get_recommendations(
    recommenderArn=recommender_top_picks_arn,
    userId=test_user_id,
    numResults=20
)

# Build a new dataframe for the recommendations
item_list = get_recommendations_response['itemList']
recommendation_list = []
for item in item_list:
    movie = get_movie_by_id(item['itemId'], items_df)
    recommendation_list.append(movie)

column_name = test_user_id+" ("+get_gender_by_id(test_user_id, users_data_df)+")"

user_recommendations_df1 = pd.DataFrame(recommendation_list, columns = [column_name])

pd.options.display.max_rows =20
print('Top picks for user ' + test_user_id)
print('*******************************')
print(user_recommendations_df1)