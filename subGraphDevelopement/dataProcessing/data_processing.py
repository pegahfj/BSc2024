import os
import logging
from gSpanAlgorithm.gSpan.gspan_mining import gSpan


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def reformat_data(data_dict, output_dir):
    """
    Iterates through all datasets in the data dictionary, processes them, and saves the formatted data.

    Parameters:
    - data_dict (dict): Dictionary with dataset names as keys and 4D numpy arrays as values.
    - output_dir (str): Base directory where all formatted datasets will be saved.
    """
    try:
        ensure_directory_exists(output_dir)
        for dataset_name, dataset in data_dict.items():
            logging.info(f"Processing dataset: {dataset_name}")
            dataset_dir = os.path.join(output_dir, dataset_name)
            ensure_directory_exists(dataset_dir)
            process_dataset(dataset, dataset_dir)
    except Exception as e:
        logging.error(f"Error in reformat_data: {e}")

def process_dataset(dataset, dataset_dir):
    """
    Processes a single dataset, formatting the data for all patients and saving it.

    Parameters:
    - dataset (numpy.ndarray): 4D array (patients x vertices x vertices x windows).
    - dataset_dir (str): Directory where the dataset's folder will be created.
    """
    try:
        num_patients = dataset.shape[0]  # Number of patients

        for patient_idx in range(num_patients):
            # Extract data for the patient and process
            patient_data = dataset[patient_idx]

            # Extract matrices for all time windows
            patient_time_series = [patient_data[:, :, w] for w in range(patient_data.shape[2])] # List of 2D matrices

            # Format graphs for all matrices of this patient
            formatted_data = reformat_graph(patient_idx, patient_time_series)

            # Create a subdirectory for the patient
            patient_dir = os.path.join(dataset_dir, f"patient_{patient_idx}")
            ensure_directory_exists(patient_dir)

            # Save the formatted data to a file within the patient's subdirectory
            output_file = os.path.join(patient_dir, f"patient_{patient_idx}.txt")
            with open(output_file, 'w') as f:
                f.write("\n".join(formatted_data))
            logging.info(f"Saved formatted data for patient {patient_idx} in {output_file}")
    except Exception as e:
        logging.error(f"Error in process_dataset: {e}")

def reformat_graph(subject_idx, matrices, edge_threshold=1, vertex_label=1000):
    """
    Formats graphs for a single subject across multiple matrices (time windows).

    Parameters:
    - subject_idx (int): Subject index to label the graphs.
    - matrices (list of numpy.ndarray): List of 2D matrices (e.g., 19x19 per time window).
    - edge_threshold (float): Minimum weight for including an edge.
    - vertex_label (int): Arbitrary label for all vertices.

    Returns:
    - list: A list of strings representing multiple graphs for the subject.
    """
    try:
        formatted_data = []

        for window_idx, matrix in enumerate(matrices):
            formatted_data.append(f"t # {subject_idx}_{window_idx}")  # Graph identifier (subject + window)

            num_vertices = matrix.shape[0]  # Number of vertices
            # Add vertex information with unique labels
            for vertex in range(num_vertices):
                formatted_data.append(f"v {vertex} {vertex}")  # Unique label for each vertex is its index

            # Add edge information
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if i != j:
                        edge_value = matrix[i, j]
                        # Include edge only if it exceeds the threshold, with neutral value as the label
                        edge_label = 3 if edge_value > edge_threshold else 2
                        formatted_data.append(f"e {i} {j} {edge_label}")

        # Add end of graph definition for each matrix
        formatted_data.append("t # -1")

        return formatted_data
    except Exception as e:
        logging.error(f"Error in reformat_graph: {e}")
        return []

def ensure_directory_exists(directory_path):
    """
    Ensures the given directory exists. Creates it if it doesn't.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logging.info(f"Created directory: {directory_path}")
    except Exception as e:
        logging.error(f"Error in ensure_directory_exists: {e}")

def run_gspan_on_patients(condition_path, params):
    """
    Iterates over each patient's folder and runs gSpan on their data files.

    Parameters:
    - condition_path (str): The directory containing all patient data folders.
    - params (dict): Parameters for the gSpan command.
    """
    try:
        # Iterate through each patient folder within the condition
        for patient in os.listdir(condition_path):
            patient_path = os.path.join(condition_path, patient)
            logging.info(f"Find the data file for the patient_path: {patient_path}")

            if not os.path.isdir(patient_path):
                logging.warning(f"Skipping non-directory entry: {patient_path}")
                continue

            # Find the data file for the patient
            for file in os.listdir(patient_path):
                if file.endswith(".txt"):
                    input_file = os.path.join(patient_path, file)
                    logging.info(f"Find the data file for the patient: {input_file}")

                    # Initialize and run gSpan
                    gs = gSpan(
                        database_file_name=input_file,
                        min_support=params["min_support"],
                        min_num_vertices=params["min_num_vertices"],
                        max_num_vertices=params.get("max_num_vertices", float('inf')),
                        max_ngraphs=params.get("max_ngraphs", float('inf')),
                        is_undirected=not params["is_directed"],
                        verbose=params.get("verbose", False),
                        visualize=params["visualize"],
                        where=params["where"]
                    )
                    gs.run()
                    gs.time_stats()
                    gs.save_results(input_file)
    except Exception as e:
        logging.error(f"Error in run_gspan_on_patients: {e}")