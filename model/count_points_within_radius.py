import numpy as np

def count_points_within_radius(X1, Y1, X2, Y2, radius):
    X1 = np.array(X1)
    Y1 = np.array(Y1)
    X2 = np.array(X2)
    Y2 = np.array(Y2)
    # Calculate the distances between each pair of points
    distances = np.sqrt(((X1[:, np.newaxis] - X2)*111)**2 + ((Y1[:, np.newaxis] - Y2)*101)**2)

    # Count the number of points within the radius threshold
    count = np.sum(distances <= radius/1000, axis=1)

    return count