import os
import subprocess

def run_gspan(patient_file_path, output_dir):
    # Define the gSpan command template
    gspan_command_template = "python -m gspan_mining -s {min_support} -d {is_directed} -l {min_num_vertices} -p {visualize} -w {where} -o {output_file} {patient_file}"

    # Define the gSpan parameters
    params = {
        "min_support": 30,
        "is_directed": True,
        "min_num_vertices": 3,
        "visualize": False,
        "where": True
    }

    # Construct the output file path
    output_file = os.path.join(output_dir, f"subgraph_{os.path.basename(patient_file_path)}")

    # Pass the patient file directly to the gSpan command
    command = gspan_command_template.format(
        min_support=params["min_support"],
        min_num_vertices=params["min_num_vertices"],
        is_directed=params["is_directed"],
        visualize=params["visualize"],
        where=params["where"],
        output_file=output_file,
        patient_file=patient_file_path
    )
    print(f"Running gSpan command: {command}")
    subprocess.run(command, shell=True)

def main():
    # Step 1: Define the directory containing the patient files
    processed_data_dir = "/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/processedData"

    # Step 2: Iterate over directories inside the processedData directory
    for group_sample in os.listdir(processed_data_dir):
        group_sample_dir_path = os.path.join(processed_data_dir, group_sample)
        
        if not os.path.isdir(group_sample_dir_path):
            print(f'src_data: {group_sample_dir_path} was not found!')
            continue

        # Create output directory for subgraphs
        output_category_dir = os.path.join(processed_data_dir, "subgraphs", group_sample)
        os.makedirs(output_category_dir, exist_ok=True)

        # Step 3: Iterate over each patient's data file in the group sample directory
        for patient_file in os.listdir(group_sample_dir_path):
            patient_file_path = os.path.join(group_sample_dir_path, patient_file)
            if not os.path.isfile(patient_file_path):
                continue

            # Step 4: Run gSpan on the patient's data file
            try:
                print(f"Running gSpan on patient file: {patient_file_path}")
                run_gspan(patient_file_path, output_category_dir)
                print("gSpan execution complete.")
            except Exception as e:
                print(f"Error running gSpan on {patient_file_path}: {e}")
                continue

if __name__ == '__main__':
    main()
