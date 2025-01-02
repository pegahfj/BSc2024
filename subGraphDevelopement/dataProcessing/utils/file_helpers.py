import numpy as np

def save_matrix_to_file(matrix, file_path):
    """
    Saves a matrix to a file in text format.
    """
    with open(file_path, 'w') as f:
        np.savetxt(f, matrix, fmt='%.6f')

def load_npy_as_dict(file_path):
    """
    Loads a `.npy` file as a dictionary.
    """
    return np.load(file_path, allow_pickle=True).item()