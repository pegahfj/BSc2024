from .process_data import export_transformed_datastructure, run_gspan_on_patients, export_patient_merged_subgraphs, check_vertex_labels
from .load_data import load_patients_EEG_data

from gSpanAlgorithm.gSpan.gspan_mining import gSpan

import os
import logging
from contextlib import redirect_stdout

def run_gspan(base_dir):

    params = {
        "min_support": 60,
        "is_directed": True,
        "min_num_vertices": 3,
        "visualize": False,
        "where": True
    }
   
    # Iterate through each condition folder
    for condition in os.listdir(base_dir):
        condition_path = os.path.join(base_dir, condition)
        if not os.path.isdir(condition_path):
            print(f"Skipping non-directory entry condition_path: {condition_path}")
            continue
    run_gspan_on_patients(condition_path, params)

def main():
    # Step 1: Define paths and parameters
    input_dir = "/Users/pegz/Desktop/BSc2024/sourceData/"
    output_dir = "/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/processedData"
    vertex_labels_file = '/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/dataProcessing/vertex_labels_check.txt'
    gspan_output_file = '/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/dataProcessing/gspan_output.txt'

    # Step 2: Load data
    try:
        print("Loading data...")
        data_dict = load_patients_EEG_data(input_dir)
        print("Data loading complete.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Step 3: Process and save formatted data
    try:
        print("Processing and formatting data...")
        export_transformed_datastructure(data_dict, output_dir)
        print("Data processing complete.")
    except Exception as e:
        print(f"Error processing data: {e}")
        return

    # Step 4: Run gSpan on each patient data
    try:
        print(f"Running gSpan...")
        with open(gspan_output_file, 'w') as f:
            with redirect_stdout(f):
                run_gspan(output_dir)
        print("gSpan execution complete.")
    except Exception as e:
        print(f"Error running gSpan on {output_dir}: {e}")

    # Step 5: weighted graph
    try:
        print("Creating weighted graph...")
        export_patient_merged_subgraphs(output_dir)
        print("Weighted graph creation complete.")
    except Exception as e:
        print(f"Error creating weighted graph: {e}")
        return
    check_vertex_labels(output_dir, vertex_labels_file)

if __name__ == '__main__':
    main()