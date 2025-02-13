from flask import Flask, request, jsonify
from flask_cors import CORS
from upload import upload_bp
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(upload_bp, url_prefix="/upload") 

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask server is running"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)