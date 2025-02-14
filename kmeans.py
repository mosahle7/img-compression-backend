import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import Image
import os

PROCESSED_FOLDER = "processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def apply_kmeans(img_path, K=64):
    """ Apply K-Means clustering to compress the image """
    og_img = Image.open(img_path).convert("RGB")  # Ensure RGB format
    og_img = np.array(og_img)

    X_img = np.reshape(og_img, (og_img.shape[0] * og_img.shape[1], 3)).astype(np.float32)

    # Scale only if required (JPEG needs scaling, PNG doesn't)
    if X_img.max() > 1:
        X_img /= 255.0

    kmeans = KMeans(n_clusters=K, init="k-means++", max_iter=100, random_state=42, algorithm='elkan')
    kmeans.fit(X_img)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    centroids = (centroids * 255).astype(np.uint8)
    X_recovered = centroids[labels]
    X_recovered = np.reshape(X_recovered, og_img.shape)

    compressed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(img_path))
    cv2.imwrite(compressed_path, cv2.cvtColor(X_recovered, cv2.COLOR_RGB2BGR))

    return compressed_path
