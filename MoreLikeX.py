import boto3
import pandas as pd

items_df = pd.read_csv('C:/Users/Andzej/Desktop/ml-latest-small/movies.csv')
items_df.sample(10)

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')
recommender_more_like_x_arn = 'arn:aws:personalize:us-east-1:217528143255:recommender/more_like_x'

def get_movie_by_id(movie_id, movie_df):
    try:
        return movie_df.loc[movie_df["movieId"] == int(movie_id)]['title'].values[0]
    except:
        print(movie_id)
        return "Error obtaining title"


# First pick a user
test_user_id = "1"

# Select a random item
test_item_id = "50"

# Get recommendations for the user for this item
get_recommendations_response = personalize_runtime.get_recommendations(
    recommenderArn=recommender_more_like_x_arn,
    itemId=test_item_id,
    userId=test_user_id,
    numResults=20
)

# Build a new dataframe for the recommendations
item_list = get_recommendations_response['itemList']
recommendation_list = []
for item in item_list:
    movie = get_movie_by_id(item['itemId'], items_df)
    recommendation_list.append(movie)

user_recommendations_df = pd.DataFrame(recommendation_list, columns=[get_movie_by_id(test_item_id, items_df)])

pd.options.display.max_rows = 20
print(user_recommendations_df)



