from flask import Flask, jsonify, request
from assistant import Assistant


app = Flask(__name__)
assistant = Assistant(update_shops=True)


@app.route('/user_imprint', methods=['POST'])
def get_user_imprint():
    content = request.args.get('content', [])
    fav_shops = request.args.get('fav_shops', [])
    user_imprint = assistant.form_user_imprint(content, fav_shops)
    return jsonify({'user_imprint': user_imprint})


@app.route('/user_imprint', methods=['POST'])
def get_recommendations():
    user_imprint = request.args.get('user_imprint')
    banned_shops = request.args.get('banned_shops', [])
    count = request.args.get('count', 3)

    items = assistant.make_recommendation(user_imprint, banned_shops, count)
    return jsonify({'items': items})


@app.route('/search', methods=['POST'])
def get_serp():
    user_imprint = request.args.get('user_imprint')
    question = request.args.get('request')
    count = request.args.get('count', 3)

    items = assistant.make_search(user_imprint, question, count)
    return jsonify({'items': items})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
