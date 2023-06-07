from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from flask_cors import CORS, cross_origin
import json
#from werkzeug.serving import run_simple



app = Flask(__name__)
# Configure basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'admin'  # Replace with your desired username
app.config['BASIC_AUTH_PASSWORD'] = 'Admin123'  # Replace with your desired password
basic_auth = BasicAuth(app)

CORS(app)
# API endpoint to retrieve metrics

@app.route('/', methods=['GET'])
@cross_origin()
def test():
    return jsonify("You are connected!")


@app.route('/metrics', methods=['POST', 'OPTIONS'])
@cross_origin()
#@basic_auth.required
def get_metrics():
    with open('best_metrics.json', 'r') as file:
        best_metrics = json.load(file)
    return jsonify(best_metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# if __name__ == '__main__':
#     run_simple('0.0.0.0', 5001, app, use_reloader=True, use_debugger=True)
