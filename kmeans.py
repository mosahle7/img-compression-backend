import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


def apply_kmeans(image, K=64):
    """ Apply K-Means clustering to compress the image """
    image = image.convert("RGB")
    img_array = np.array(image)

    X_img = np.reshape(img_array, (img_array.shape[0] * img_array.shape[1], 3)).astype(np.float32)

    # Scale only if required (JPEG needs scaling, PNG doesn't)
    if X_img.max() > 1:
        X_img /= 255.0

    kmeans = KMeans(n_clusters=K, init="k-means++", max_iter=100, random_state=42, algorithm='elkan')
    kmeans.fit(X_img)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    centroids = (centroids * 255).astype(np.uint8)
    X_recovered = centroids[labels]
    X_recovered = np.reshape(X_recovered, img_array.shape)

    return Image.fromarray(X_recovered)
