# print(flask.__version__)
from flask import Flask, jsonify, request
from model import generate_recommendations, generate_trending_games
from flask_cors import CORS

app = Flask(__name__)
# model_knn = pickle.load(open('model pkl/model_knn.pkl', 'rb'))
# user_item_matrix = pickle.load(open('model pkl/user_item_matrix.pkl', 'rb'))
# unique_merged_df = pd.read_csv('model pkl/unique_merged_df.csv')

# setting up CORS to establish connection from vue to flask
CORS(app, resources={r"/*": {"origins": "*"}})

# @app.route('/login', methods=['GET', 'POST'])
# def handle_login():
#     if request.method == 'POST':
#         un = request.form.get('username')
#         pw = request.form.get('password')
#         if un in data and data[un] == pw:
#             return render_template('answer.html', username=un)
#         else:
#             return '<h1> Username or password is wrong ! </h1>'
#     else:
#         return render_template('login.html')


@app.route('/results', methods=['GET', 'POST'])
def final_results():
    response_object = {'status': 'SUCCESS'}
    if request.method == 'POST':
        # getting data from frontend
        post_data = request.get_json()
        game = post_data.get('gameName')

        if game:
            chosen, recom1, recom2 = generate_recommendations(game)

            if recom1 and recom2:
                response_object['similar_games'] = recom1
                response_object['also_played_games'] = recom2
            elif recom1:
                response_object['similar_games'] = recom1
                response_object['also_played_games'] = 'e'
            elif recom2:
                response_object['similar_games'] = 'e'
                response_object['also_played_games'] = recom2
            else:
                response_object['similar_games'] = 'e'
                response_object['also_played_games'] = 'e'

            response_object['chosen_one'] = chosen

        return jsonify(response_object)


@app.route('/trend')
def send_trending_games():
    response_object = {'status': 'SUCCESS',
                       'payload': generate_trending_games()}

    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True)
