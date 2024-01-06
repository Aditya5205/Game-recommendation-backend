import pickle
# import numpy as np
import pandas as pd
from random import shuffle

# reducing memory of the data_set
# def reduce_mem_usage(df):
#     """ iterate through all the columns of a dataframe and modify the data type
#         to reduce memory usage.
#     """
#     start_mem = df.memory_usage().sum() / 1024 ** 2
#     # print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
#
#     for col in df.columns:
#         col_type = df[col].dtype
#
#         if col_type != object and col_type != bool:
#             c_min = df[col].min()
#             c_max = df[col].max()
#             if str(col_type)[:3] == 'int':
#                 if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
#                     df[col] = df[col].astype(np.int8)
#                 elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
#                     df[col] = df[col].astype(np.int16)
#                 elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
#                     df[col] = df[col].astype(np.int32)
#                 elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
#                     df[col] = df[col].astype(np.int64)
#             else:
#                 if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
#                     df[col] = df[col].astype(np.float16)
#                 elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
#                     df[col] = df[col].astype(np.float32)
#                 else:
#                     df[col] = df[col].astype(np.float64)
#
#     end_mem = df.memory_usage().sum() / 1024 ** 2
#     # print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
#     # print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
#
#     return df


# importing all datasets and models

cosine_similarities = pickle.load(open('model pkl/Content_based_new/cosine_similarities_new.pkl', 'rb'))
content_based_df = pd.read_csv('model pkl/Content_based_new/content_based_df_new_20k.csv')

collaborative_df = pd.read_csv('model pkl/collaborative_df_all.csv')
model_knn = pickle.load(open('model pkl/model_knn.pkl', 'rb'))
user_item_matrix = pickle.load(open('model pkl/user_item_matrix.pkl', 'rb'))

trending_df = pd.read_csv('model pkl/trending_df.csv')


def generate_recommendations(game_name):

    # content-based
    content_recommendations = []
    if game_name in list(content_based_df.Title):
        game_index = content_based_df[content_based_df['Title'] == game_name].index[0]

        game_list = sorted(list(enumerate(cosine_similarities[game_index])), reverse=True, key=lambda x: x[1])[1:6]

        for ind in game_list:
            content_recommendations.append({
                'Name': content_based_df['Title'].iloc[ind[0]],
                'Price': content_based_df['Original Price'].iloc[ind[0]],
                'Description': content_based_df['Game Description'].iloc[ind[0]]
            })

    # collaborative
    collaborative_recommendations = []
    if game_name in list(collaborative_df.title):
        game_index = collaborative_df[collaborative_df['title'] == game_name].index[0]

        indices = model_knn.kneighbors(user_item_matrix.getrow(game_index), n_neighbors=6, return_distance=False)

        for ind in indices.flatten()[1:]:
            collaborative_recommendations.append({
                'Name': collaborative_df['title'].iloc[ind],
                'Price': collaborative_df['price_final'].iloc[ind],
                'Description': collaborative_df['description'].iloc[ind]
            })

    return content_recommendations,collaborative_recommendations


def generate_trending_games():
    ans = []
    for i in range(12):
        _id = trending_df.iloc[i]['app_id']
        img_link = 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(_id) + '/header.jpg'

        ans.append({
            'Name': trending_df.iloc[i]['Title'],
            'Price': trending_df.iloc[i]['Original Price'],
            'Image': img_link,
            'Steam': trending_df.iloc[i]['Link']
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