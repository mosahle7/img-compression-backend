from flask import Blueprint, request, jsonify, send_file    
from PIL import Image
import os
import io
import numpy as np
import base64
from kmeans import apply_kmeans

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    image = Image.open(io.BytesIO(file.read()))
    processed_image  = apply_kmeans(image)
    
    img_io = io.BytesIO()
    processed_image.save(img_io, "PNG")
    img_io.seek(0)
    
    compressed_size = len(img_io.getvalue())/1024;
    
    return jsonify({
        "image_url": "data:image/png;base64," + base64.b64encode(img_io.getvalue()).decode("utf-8"),
        "size": round(compressed_size, 2),
        "name": file.filename + "_compressed.png"
    })
    
    