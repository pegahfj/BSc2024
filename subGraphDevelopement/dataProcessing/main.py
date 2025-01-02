from data_loading import load_patients_EEG_data
from data_processing import reformat_data, run_gspan_on_patients
import os

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
    output_dir = "/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/processedData"


    # Step 2: Load data
    try:
        print("Loading data...")
        # data_dict = load_patients_EEG_data()
        print("Data loading complete.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Step 3: Process and save formatted data
    try:
        print("Processing and formatting data...")
        # reformat_data(data_dict, output_dir)
        print("Data processing complete.")
    except Exception as e:
        print(f"Error processing data: {e}")
        return

    # Step 4: Run gSpan on each patient data
    try:
        print(f"Running gSpan...")
        run_gspan(output_dir)
        print("gSpan execution complete.")
    except Exception as e:
        print(f"Error running gSpan on {output_dir}: {e}")


if __name__ == '__main__':
    main()