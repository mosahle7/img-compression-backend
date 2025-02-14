from flask import Blueprint, request, jsonify, send_file    
import os
from kmeans import apply_kmeans

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLFER = "uploads"
os.makedirs(UPLOAD_FOLFER, exist_ok=True)

@upload_bp.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLFER, file.filename)
    file.save(file_path)
    
    compressed_image_path = apply_kmeans(file_path)
    
    return send_file(compressed_image_path, mimetype="image/png")
    