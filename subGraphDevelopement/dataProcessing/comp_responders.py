import os
import json
import networkx as nx
import numpy as np
import logging
import matplotlib.pyplot as plt
from networkx.algorithms.similarity import graph_edit_distance


def load_graph(file_path):
    """
    Load a graph from a JSON file and convert it to a NetworkX graph.

    Parameters:
    - file_path (str): The path to the graph file.

    Returns:
    - nx.Graph: The loaded NetworkX graph, or None if the file is not found or empty.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None

    with open(file_path, 'r') as file:
        data = json.load(file)
        if not data.get("nodes") or not data.get("links"):
            logging.error(f"Graph data is empty in file: {file_path}")
            return None
        return nx.node_link_graph(data, edges="links")


def compare_patient_graphs(graph_day0, graph_day7):
    """
    Compare two NetworkX graphs and return comparison results.

    Parameters:
    - graph_day0 (nx.Graph): The day 0 graph.
    - graph_day7 (nx.Graph): The day 7 graph.

    Returns:
    - dict: A dictionary with comparison results.
    """
    comparison_results = {}

    # Structural comparison
    nodes_day0 = set(graph_day0.nodes())
    nodes_day7 = set(graph_day7.nodes())
    edges_day0 = set(graph_day0.edges())
    edges_day7 = set(graph_day7.edges())

    comparison_results['node_overlap'] = len(nodes_day0 & nodes_day7) / len(nodes_day0 | nodes_day7)
    comparison_results['edge_overlap'] = len(edges_day0 & edges_day7) / len(edges_day0 | edges_day7)

    # Degree distribution
    degree_day0 = [d for _, d in graph_day0.degree()]
    degree_day7 = [d for _, d in graph_day7.degree()]
    comparison_results['degree_mean_diff'] = np.mean(degree_day7) - np.mean(degree_day0)

    # Graph Edit Distance
    ged = graph_edit_distance(graph_day0, graph_day7)
    comparison_results['graph_edit_distance'] = ged

    return comparison_results


def plot_brain_graph(G, title, channel_to_region, positions, output_path=None):
    """
    Plots the graph using a schematic brain layout with fixed node positions.
    
    Parameters:
    - G (nx.DiGraph): The graph to plot.
    - title (str): The title of the plot.
    - channel_to_region (dict): Mapping of channel numbers to brain regions.
    - positions (dict): Fixed positions for brain regions.
    - output_path (str): Optional path to save the plot as an image.
    """

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")

    # Draw the circular background
    circle = plt.Circle((0, 0), 1.2, color="blue", fill=False, linewidth=2)
    ax.add_artist(circle)

    # Add all nodes from channel_to_region to the graph
    for node in channel_to_region.keys():
        if node not in G:
            G.add_node(node)

    # Map numeric channels to brain region labels
    node_labels = {node: f"{channel_to_region[node]}" for node in G.nodes()}

    # Map node positions using brain region positions
    node_positions = {node: positions[channel_to_region[node]] for node in G.nodes()}

    # Draw the graph on the same axis
    nx.draw(
        G,
        pos=node_positions,
        labels=node_labels,
        with_labels=True,
        node_size=500,
        node_color="skyblue",
        font_size=8,
        font_color="black",
        edge_color="gray",
        width=[G[u][v]["weight"] for u, v in G.edges()],
        ax=ax  # Draw on the same axis
    )

    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_labels, font_size=6, ax=ax)
    
    # Add title
    plt.title(title)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    plt.axis("off")  
    
    # Save plot if output path is specified
    if output_path:
        plt.savefig(output_path)
        print(f"Graph saved at: {output_path}")
    
    # Close the plot to avoid displaying it
    plt.close()


def visualize_patient_graphs(graph_day0, graph_day7, patient, channel_to_region, positions, output_dir):
    """
    Visualize the graphs for a patient using a schematic brain layout.

    Parameters:
    - graph_day0 (nx.Graph): The day 0 graph.
    - graph_day7 (nx.Graph): The day 7 graph.
    - patient (str): The patient identifier.
    - channel_to_region (dict): Mapping of channel numbers to brain regions.
    - positions (dict): Fixed positions for brain regions.
    - output_dir (str): Directory to save the plots.
    """
    output_path_day0 = os.path.join(output_dir, f"{patient}_day0.png")
    output_path_day7 = os.path.join(output_dir, f"{patient}_day7.png")

    plot_brain_graph(graph_day0, f"{patient} - Day 0", channel_to_region, positions, output_path_day0)
    plot_brain_graph(graph_day7, f"{patient} - Day 7", channel_to_region, positions, output_path_day7)

    # Display side-by-side plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    img_day0 = plt.imread(output_path_day0)
    img_day7 = plt.imread(output_path_day7)

    axes[0].imshow(img_day0)
    axes[0].set_title(f"{patient} - Day 0")
    axes[0].axis("off")

    axes[1].imshow(img_day7)
    axes[1].set_title(f"{patient} - Day 7")
    axes[1].axis("off")



def save_results(patient, results, output_dir):
    """
    Save the comparison results to a JSON file.

    Parameters:
    - patient (str): The patient identifier.
    - results (dict): The comparison results.
    - output_dir (str): The directory to save the results.
    """
    output_file = os.path.join(output_dir, f"{patient}_comparison_results.json")
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)
    logging.info(f"Comparison results saved for {patient} at {output_file}")


if __name__ == "__main__":

    channel_to_region = {
        1: "Fp1",
        2: "Fp2",
        3: "F3",
        4: "F4",
        5: "C3",
        6: "C4",
        7: "P3",
        8: "P4",
        9: "O1",
        10: "O2",
        11: "F7",
        12: "F8",
        13: "T3",
        14: "T4",
        15: "T5",
        16: "T6",
        17: "Fz",
        18: "Cz",
        19: "Pz"
    }

    positions = {
        "Fp1": (-0.4, 1),    # Top center
        "Fp2": (0.4, 1),
        "F7": (-0.8, 0.6),
        "F8": (0.8, 0.6),
        "F3": (-0.4, 0.7),
        "F4": (0.4, 0.7),
        "T3": (-1, 0),
        "T4": (1, 0),
        "C3": (-0.6, 0),
        "C4": (0.6, 0),
        "T5": (-0.8, -0.7),
        "T6": (0.8, -0.7),
        "P3": (-0.6, -0.6),
        "P4": (0.6, -0.6),
        "O1": (-0.4, -1),
        "O2": (0.4, -1),
        "Fz": (0, 0.7),
        "Cz": (0, 0),
        "Pz": (0, -0.6)
    }
    base_dir_day0 = "/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/processedData/alpha_responder_day0"  # Update with your directory path
    base_dir_day7 = "/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/processedData/alpha_responder_day7"  # Update with your directory path
    output_dir = "/Users/pegz/Desktop/BSc2024/BSc2024/subgraphDevelopement/dataProcessing/comparison_results"  # Directory to save results

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for patient in os.listdir(base_dir_day0):
        print(f"\nProcessing {patient}...")

        # Construct file paths
        patient_day0 = os.path.join(base_dir_day0, f"{patient}/{patient}_weighted_graph_positive.json")
        patient_day7 = os.path.join(base_dir_day7, f"{patient}/{patient}_weighted_graph_positive.json")

        # Check if files exist
        if not os.path.exists(patient_day0) or not os.path.exists(patient_day7):
            print(f"Skipping {patient} due to missing files.")
            continue

        # Load graphs
        graph_day0 = load_graph(patient_day0)
        graph_day7 = load_graph(patient_day7)

        # Check if graphs are loaded successfully
        if graph_day0 is None or graph_day7 is None:
            print(f"Skipping {patient} due to missing or empty graph.")
            continue

        # Compare graphs
        results = compare_patient_graphs(graph_day0, graph_day7)
        print(f"Comparison Results for {patient}:", results)

        # Save results
        save_results(patient, results, output_dir)

        # Visualize graphs
        visualize_patient_graphs(graph_day0, graph_day7, patient, channel_to_region, positions, output_dir)