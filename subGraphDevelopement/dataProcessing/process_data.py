from gSpanAlgorithm.gSpan.gspan_mining import gSpan
import os
import logging
import networkx as nx
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def export_transformed_datastructure(data_dict, output_dir):
    """
    Iterates through all datasets in the data dictionary, processes them, and saves the formatted data.

    Parameters:
    - data_dict (dict): Dictionary with dataset names as keys and 4D numpy arrays as values.
    - output_dir (str): Base directory where all formatted datasets will be saved.
    """
    try:
        ensure_directory_exists(output_dir)
        for dataset_name, dataset in data_dict.items():
            logging.info(f"transforming dataset: {dataset_name}")
            dataset_dir = os.path.join(output_dir, dataset_name)
            ensure_directory_exists(dataset_dir)
            transform_original_dataset_structure(dataset, dataset_dir)
    except Exception as e:
        logging.error(f"Error in export_transformed_datastructure: {e}")

def transform_original_dataset_structure(dataset, dataset_dir):
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
            formatted_data = transform_patient_timeseries_matrices(patient_idx, patient_time_series)

            # Create a subdirectory for the patient
            patient_dir = os.path.join(dataset_dir, f"patient_{patient_idx}")
            ensure_directory_exists(patient_dir)

            # Save the formatted data to a file within the patient's subdirectory
            output_file = os.path.join(patient_dir, f"patient_{patient_idx}.txt")
            with open(output_file, 'w') as f:
                f.write("\n".join(formatted_data))
            logging.info(f"Saved transformed data for patient {patient_idx} in {output_file}")
    except Exception as e:
        logging.error(f"Error in transform_original_dataset_structure: {e}")

def transform_patient_timeseries_matrices(subject_idx, matrices, edge_threshold=0, vertex_label=1000):
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
            formatted_data.append(f"t # {subject_idx}{window_idx}")  # Graph identifier (subject + window)

            num_vertices = matrix.shape[0]  # Number of vertices
            # Add vertex information with unique labels
            for vertex in range(num_vertices):

                vertex_label = vertex +1 # Unique label for each vertex is its index +2 : labels>1
                if vertex < 0 or vertex > 18:
                    logging.error(f"Vertex out of range: {vertex_label} patient: {subject_idx} window: {window_idx}")
                if  vertex_label > 19:
                    logging.error(f"Vertex label out of range: {vertex_label} patient: {subject_idx} window: {window_idx}")
                formatted_data.append(f"v {vertex} {vertex_label}") 
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

def parse_subgraph_motifs(subgraph_file_path):
    """
    parse_subgraph_motifs function reads subgraph_file containing subgraph motifs and parses its content 
    into a list(motifs = []) of motif dictionaries. Each motif dictionary contains vertices, edges, 
    and support information. The function opens the subgraph_file produced by gSpan, reads all lines, 
    and iterates through them. It identifies different parts of the motif based on line prefixes ('t #', 
    'v', 'e', 'Support:') and constructs the motif dictionary accordingly. Once all lines are processed, 

    Returns: 
    - list: of motifs.
    """
    motifs = []
    with open(subgraph_file_path, 'r') as file:
        lines = file.readlines()
        motif = None
        for line in lines:
            if line.startswith('t #'):
                if motif:
                    motifs.append(motif)
                motif = {'vertices': {}, 'edges': [], 'support': 0}
            elif line.startswith('v'):
                parts = line.split()
                vertex_id = int(parts[1])
                vertex_label = int(parts[2])
                motif['vertices'][vertex_id] = vertex_label
            elif line.startswith('e'):
                parts = line.split()
                motif['edges'].append((int(parts[1]), int(parts[2]), int(parts[3])))
            elif line.startswith('Support:'):
                motif['support'] = int(line.split()[1])
        if motif:
            motifs.append(motif)
    return motifs

def build_weighted_directed_graph(motifs):
    """
    Builds two weighted directed graphs from the given motifs: one for positive edges and one for negative edges.

    Parameters:
    - motifs (list): A list of motif dictionaries.

    Returns:
    - tuple: Two NetworkX DiGraph objects, one for positive edges and one for negative edges.
    """
    G_positive = nx.DiGraph()
    G_negative = nx.DiGraph()
    
    for motif in motifs:
        vertices = motif['vertices']
        for edge in motif['edges']:
            frm_id, to_id, label = edge
            frm_label = vertices[frm_id]
            to_label = vertices[to_id]
            
            if label == 3:  # Positive edge
                if G_positive.has_edge(frm_label, to_label):
                    G_positive[frm_label][to_label]['weight'] += 1
                else:
                    G_positive.add_edge(frm_label, to_label, weight=1, label=label)
            elif label == 2:  # Negative edge
                if G_negative.has_edge(frm_label, to_label):
                    G_negative[frm_label][to_label]['weight'] += 1
                else:
                    G_negative.add_edge(frm_label, to_label, weight=1, label=label)
    
    return G_positive, G_negative

def export_patient_merged_subgraphs(base_dir):
    """
    Processes patient data stored in a directory structure, builds weighted directed graphs, and saves them as JSON files.

    Parameters:
    - base_dir (str): The base directory containing patient data.
    """
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if not os.path.isdir(category_path):
            continue
        for patient in os.listdir(category_path):
            patient_path = os.path.join(category_path, patient)
            if not os.path.isdir(patient_path):
                continue
            subgraph_file = os.path.join(patient_path, f"{patient}_subgraphs.txt")
            if not os.path.isfile(subgraph_file):
                continue
            motifs = parse_subgraph_motifs(subgraph_file)
            
            G_positive, G_negative = build_weighted_directed_graph(motifs)
            
            output_file_js_positive = os.path.join(patient_path, f"{patient}_weighted_graph_positive.json")
            output_file_js_negative = os.path.join(patient_path, f"{patient}_weighted_graph_negative.json")
            
            save_graph_as_json(G_positive, output_file_js_positive)
            save_graph_as_json(G_negative, output_file_js_negative)
            

def save_graph_as_json(G, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(nx.node_link_data(G, edges="links"), json_file, indent=4)
    logging.info(f"Graph saved as JSON in {output_file}")


def check_vertex_labels(base_dir, output_file):
    """
    Iterates through all patients, checks vertex labels, and creates a text file with the numbers
    that are not in the range of 2-21 along with the patient file name.

    Parameters:
    - base_dir (str): The base directory containing patient data.
    - output_file (str): The path to the output text file.
    """
    try:
        with open(output_file, 'w') as out_file:
            for category in os.listdir(base_dir):
                category_path = os.path.join(base_dir, category)
                if not os.path.isdir(category_path):
                    continue
                for patient in os.listdir(category_path):
                    patient_path = os.path.join(category_path, patient)
                    if not os.path.isdir(patient_path):
                        continue
                    subgraph_file = os.path.join(patient_path, f"{patient}_subgraphs.txt")
                    if not os.path.isfile(subgraph_file):
                        continue
                    with open(subgraph_file, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            if line.startswith('v'):
                                parts = line.split()
                                vertex_label = int(parts[2])
                                if vertex_label < 2 or vertex_label > 19:
                                    out_file.write(f"{vertex_label} {patient} {category_path}\n")
        logging.info(f"Vertex label check completed. Results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error in check_vertex_labels: {e}")


