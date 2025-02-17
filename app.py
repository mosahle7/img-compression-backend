from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
from upload import upload_bp
import os

WSGIRequestHandler.protocol_version = "HTTP/1.1"  # Keep connection open
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"], supports_credentials=True)

app.register_blueprint(upload_bp, url_prefix="/upload") 

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask server is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000, threaded= True)