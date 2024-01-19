# import pickle
import pandas as pd
from random import shuffle
from db import access_database_chosen, access_database_content, access_database_collaborative

# importing all datasets and models
# collaborative_df = pd.read_csv('model pkl/collaborative_df_all.csv')
# model_knn = pickle.load(open('model pkl/model_knn.pkl', 'rb'))
# user_item_matrix = pickle.load(open('model pkl/user_item_matrix.pkl', 'rb'))

trending_df = pd.read_csv('model pkl/trending_df.csv')


def generate_recommendations(game_name):
    # the chosen game
    chosen_one = access_database_chosen(game_name)

    # content-based
    content_recommendations = access_database_content(game_name)

    # collaborative
    collaborative_recommendations = access_database_collaborative(game_name)

    return chosen_one, content_recommendations, collaborative_recommendations


def generate_trending_games():
    ans = []
    for i in range(12):
        game_id = trending_df.iloc[i]['app_id']

        ans.append({
            'Name': trending_df.iloc[i]['Title'],
            'Price': trending_df.iloc[i]['Original Price'],
            'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(game_id) + '/header.jpg',
            'Steam': 'https://store.steampowered.com/app/' + str(game_id)
        })

    shuffle(ans)

    return ans
