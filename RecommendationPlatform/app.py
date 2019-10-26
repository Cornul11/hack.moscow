from flask import Flask, jsonify, request
from assistant import Assistant
from shop_searcher import ShopSearcher


app = Flask(__name__)
assistant = Assistant(update_shops=True)
searcher = ShopSearcher()


@app.route('/user_imprint', methods=['POST'])
def get_user_imprint():
    args = request.json
    content = args.get('content', [])
    fav_shops = args.get('fav_shops', [])
    user_imprint = assistant.form_user_imprint(content, fav_shops)
    return jsonify({'user_imprint': user_imprint.tolist()})


@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    args = request.json
    user_imprint = args.get('user_imprint')
    banned_shops = args.get('banned_shops', [])
    count = args.get('count', 3)

    items = assistant.make_recommendation(user_imprint, banned_shops, count)
    return jsonify({'items': items})


@app.route('/search', methods=['POST'])
def get_serp():
    args = request.json
    user_imprint = args.get('user_imprint')
    question = args.get('request')
    count = request.args.get('count', 3)

    items = assistant.make_search(user_imprint, question, count)
    return jsonify({'items': items})


@app.route('/closest_shoppings', methods=['POST'])
def get_closest_shopping():
    args = request.json
    venue_id = args.get('venue_id')
    lat, lon = args.get('lat'), args.get('lon')
    count = request.args.get('count', 1)

    items = searcher.get_closest(venue_id, lat, lon, count)
    return jsonify({'items': items})


@app.route('/')
def main():
    return jsonify({'test': 'test'})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
