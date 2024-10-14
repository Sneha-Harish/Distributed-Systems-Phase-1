import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import rpyc
import time
import matplotlib.pyplot as plt
import numpy as np

def get_word_count(conn, filename, keyword):
    try:
        # First request: measure latency
        start_time = time.time()
        word_count = conn.root.exposed_word_count(filename, keyword)
        latency = time.time() - start_time
        
        # Second request: Cache hit latency
        start_time_cache = time.time()
        word_count_cache = conn.root.exposed_word_count(filename, keyword)
        cache_latency = time.time() - start_time_cache
        
        return word_count, latency, cache_latency
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0, 0, 0

def plot_metrics(latencies):

    x_labels = [pair[0] for pair in latencies]
    normal_latencies = [pair[1] for pair in latencies]
    cache_latencies = [pair[2] for pair in latencies]
    
    x = np.arange(len(x_labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart for normal and cache latencies
    bars1 = ax.bar(x - width/2, normal_latencies, width, label='Normal Latency')
    bars2 = ax.bar(x + width/2, cache_latencies, width, label='Cache Latency')

    # Add labels, title, and custom x-axis tick labels
    ax.set_xlabel("Keyword-Filename Pair")
    ax.set_ylabel("Latency (seconds)")
    ax.set_title("Normal Latency vs Cache Latency for Keyword-Filename Pairs")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45)
    ax.legend()

    # Ensure layout is tight to avoid overlap
    plt.tight_layout()

    # Save the plot as a PNG image
    plt.savefig("/output/latency_plot.png")
    print("Plot saved as /output/latency_plot.png")

if __name__ == "__main__":
    # Connect to the server
    conn = rpyc.connect("wordcount_server_1", 18812)
    print("Connection successful!")
    
    # Ask the user for the number of keyword-filename pairs
    num_pairs = int(input("Enter the number of keyword-filename pairs: "))
    
    keyword_filename_pairs = []
    
    # Get all keyword-filename pairs from the user at once
    for _ in range(num_pairs):
        keyword = input("Enter the keyword: ")
        filename = input("Enter the filename: ")
        keyword_filename_pairs.append((filename, keyword))
    
    latencies = []  # To store latencies for plotting
    
    for filename, keyword in keyword_filename_pairs:
        # Make the calls and measure latencies
        word_count, latency, cache_latency = get_word_count(conn, filename, keyword)
        
        print(f"The keyword '{keyword}' appears {word_count} times in {filename}.")
        print(f"First request latency: {latency} seconds")
        print(f"Cache hit latency: {cache_latency} seconds")
        
        # Store the latency for plotting later
        latencies.append((f"{keyword}-{filename}", latency, cache_latency))
        
        # Clear the cache for this batch
        conn.root.clear_cache()
    
    plot_metrics(latencies)
