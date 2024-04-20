# print(flask.__version__)
from flask import Flask, jsonify, request
from model import generate_recommendations, generate_trending_games
from flask_cors import CORS

app = Flask(__name__)

# setting up CORS to establish connection from vue to flask
# CORS(app, origins="http://localhost:5173/")
CORS(app, resources={r"/*": {"origins": "https://gamematrix.vercel.app"}})

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


@app.route('/results', methods=['POST'])
def final_results():
    response_object = {'status': 'SUCCESS'}

    # getting data from frontend
    post_data = request.get_json()
    game = post_data.get('gameName')

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

    if chosen:
        response_object['chosen_one'] = chosen
    else:
        response_object['chosen_one'] = 'e'

    return jsonify(response_object)


@app.route('/trend')
def send_trending_games():
    response_object = {'status': 'SUCCESS',
                       'payload': generate_trending_games()}

    return jsonify(response_object)


