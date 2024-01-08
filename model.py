import pickle
# import numpy as np
import pandas as pd
from random import shuffle

# importing all datasets and models
cosine_similarities = pickle.load(open('model pkl/Content_based_new/cosine_similarities_new.pkl', 'rb'))
content_based_df = pd.read_csv('model pkl/Content_based_new/content_based_df_new_20k.csv')

collaborative_df = pd.read_csv('model pkl/collaborative_df_all.csv')
model_knn = pickle.load(open('model pkl/model_knn.pkl', 'rb'))
user_item_matrix = pickle.load(open('model pkl/user_item_matrix.pkl', 'rb'))

trending_df = pd.read_csv('model pkl/trending_df.csv')


def generate_recommendations(game_name):

    # the chosen game
    game_ind = content_based_df[content_based_df['Title'] == game_name].index[0]
    game_id = content_based_df['app_id'].iloc[game_ind]

    game_img = 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(game_id) + '/header.jpg'
    chosen_one = [
        {
            'Image': game_img,
            'Price': content_based_df['Original Price'].iloc[game_ind],
            'Description': content_based_df['Game Description'].iloc[game_ind],
            'Steam': 'https://store.steampowered.com/app/' + str(game_id)
        }
    ]

    # content-based
    content_recommendations = []
    if game_name in list(content_based_df.Title):
        game_index = content_based_df[content_based_df['Title'] == game_name].index[0]

        game_list = sorted(list(enumerate(cosine_similarities[game_index])), reverse=True, key=lambda x: x[1])[1:6]

        for ind in game_list:
            game_id = content_based_df['app_id'].iloc[ind[0]]

            content_recommendations.append({
                'Name': content_based_df['Title'].iloc[ind[0]],
                'Price': content_based_df['Original Price'].iloc[ind[0]],
                'Description': content_based_df['Game Description'].iloc[ind[0]],
                'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(game_id) + '/header.jpg',
                'Steam': 'https://store.steampowered.com/app/' + str(game_id)
            })

    # collaborative
    collaborative_recommendations = []
    if game_name in list(collaborative_df.title):
        game_index = collaborative_df[collaborative_df['title'] == game_name].index[0]

        indices = model_knn.kneighbors(user_item_matrix.getrow(game_index), n_neighbors=6, return_distance=False)

        for ind in indices.flatten()[1:]:
            game_id = collaborative_df['app_id'].iloc[ind]

            collaborative_recommendations.append({
                'Name': collaborative_df['title'].iloc[ind],
                'Price': collaborative_df['price_final'].iloc[ind],
                'Description': collaborative_df['description'].iloc[ind],
                'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(game_id) + '/header.jpg',
                'Steam': 'https://store.steampowered.com/app/' + str(game_id)
            })

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


# list(set(game_recommendations))


# ans1 = generate_recommendations('Prince of Persia: Warrior Within™')
# common games = ['TEKKEN 7','Sniper Elite']
# ans1,ans2 = generate_recommendations('S.T.A.L.K.E.R.: Clear Sky')
# for i in ans1:
#     print(i)
# print("")
# for i in ans2:
#     print(i)

# print(generate_recommendations('Call of Duty®: Black Ops'))