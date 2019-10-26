from flask import Flask, jsonify, request
from assistant import Assistant


app = Flask(__name__)
assistant = Assistant(update_shops=True)


@app.route('/user_imprint', methods=['POST'])
def get_user_imprint():
    content = request.args.get('content')
    user_imprint = assistant.form_user_imprint(content)
    return jsonify({'user_imprint': user_imprint})


@app.route('/user_imprint', methods=['POST'])
def get_recommendations():
    user_imprint = request.args.get('user_imprint')
    banned_shops = request.args.get('banned_shops', [])
    count = request.args.get('count', 3)

    items = assistant.make_recommendation(user_imprint, banned_shops, count)
    return jsonify({'items': items})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
