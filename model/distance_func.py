import numpy as np
import pandas as pd

def get_distance_matrix(A: np.ndarray, B:np.ndarray) -> np.ndarray:
    AX = np.array(A['X'])
    AY = np.array(A['Y'])
    BX = np.array(B['X'])
    BY = np.array(B['Y'])
    # Calculate the distances between each pair of points
    distances = np.sqrt(((AX[:, np.newaxis] - BX)*111)**2 + ((AY[:, np.newaxis] - BY)*101)**2)
    return distances


def min_mask(dist_mat: np.ndarray) -> np.ndarray:
    min_values = np.min(dist_mat, axis=0)  # Find the minimum values along the columns
    comparison_matrix = dist_mat == min_values.reshape(1, -1)  # Create a boolean matrix with True where the minimum values occur
                                                                #  reshape the min_values array into a row vector.
    marked_matrix = comparison_matrix.astype(bool)  # Convert the boolean matrix to an integer matrix (0s and 1s)
    return marked_matrix

def within_dist(dist_mat:np.ndarray, distance: float) -> np.ndarray:
    return dist_mat <= distance

def accident_around_road(taipei_road, unique_accidence, dist):
    """
    Returns a matrix.
    - Row: Each intersection/ road/ roundabout
    - Column: Each accident
    
    Accidents around a collection of roads.

    dist: in meter
    """
    dist_mat = get_distance_matrix(taipei_road, unique_accidence)

    return min_mask(dist_mat) & within_dist(dist_mat, dist/1000)

def map_road_to_accident(aar_matrix, accident_pd: pd.DataFrame):
    road_indicies = np.where(aar_matrix.transpose() == 1)
    unique_accidence = accident_pd.copy()
    unique_accidence['AMPM'] = unique_accidence

    unique_accidence.loc[road_indicies[0], 'road_index'] = road_indicies[1]
