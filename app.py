import os
import hashlib
import hmac
import base64

from flask import Flask, Request, request, jsonify


app = Flask(__name__)


@app.route('/message', methods=['POST'])
def messages():
    if is_request_hmac_valid(request):
        body = request.json
        messageText = body['text']
        userName = body['from']['name']
        messageInfoStr = "{} said {}".format(userName, messageText)
        app.logger.info(messageInfoStr)

        return build_message(messageInfoStr), 200
    else:
        return "Invalid request", 400


def is_request_hmac_valid(request: Request):
    actual = request.headers.get('Authorization').replace("HMAC ", "")

    expected_hmac = hmac.new(TEAMS_SECURITY_KEY, request.data, hashlib.sha256)
    expected = base64.b64encode(expected_hmac.digest()).decode()

    if actual == expected:
        return True
    app.logger.info('Invalid HMAC')
    return False


def build_message(message: str):
    payload = {
        'type': 'message',
        'text': message
    }

    return jsonify(payload)


if __name__ == '__main__':
    TEAMS_SECURITY_KEY = base64.b64decode(os.environ.get('TEAMS_SECURITY_KEY').encode('utf-8'))
    app.run(host='0.0.0.0', port=5555, debug=True)
