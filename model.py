# import pickle
import pandas as pd
from random import shuffle
from db import access_database_chosen, access_database_content, access_database_collaborative

# importing all datasets and models
# collaborative_df = pd.read_csv('model pkl/collaborative_df_all.csv')
# model_knn = pickle.load(open('model pkl/model_knn.pkl', 'rb'))
# user_item_matrix = pickle.load(open('model pkl/user_item_matrix.pkl', 'rb'))

# trending_df = pd.read_csv('model pkl/trending_df.csv')

trending_games_data = [
    ["Monster Hunter: World", "$23.99", "9 Aug, 2018", 582010],
    ["Dota 2", "$92.62", "9 Jul, 2013", 570],
    ["Baldur's Gate 3", "$29.99", "3 Aug, 2023", 1086940],
    ["PUBG: BATTLEGROUNDS", "Free", "21 Dec, 2017", 578080],
    ["Team Fortress 2", "$10.49", "10 Oct, 2007", 440],
    ["NARAKA: BLADEPOINT", "Free", "11 Aug, 2021", 1203220],
    ["Apex Legends™", "Free", "4 Nov, 2020", 1172470],
    ["Grand Theft Auto V", "$33.98", "13 Apr, 2015", 271590],
    ["Rust", "$19.99", "8 Feb, 2018", 252490],
    ["Call of Duty®", "Free", "27 Oct, 2022", 1938090],
    ["ELDEN RING", "$34.99", "24 Feb, 2022", 1245620],
    ["Warframe", "Free", "25 Mar, 2013", 230410],
]

trending_df = pd.DataFrame(trending_games_data, columns=["Title", "Original Price", "Release Date", "app_id"])


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
