import matplotlib
matplotlib.use('Agg')

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
        
        latency_ms = latency * 1000
        cache_latency_ms = cache_latency * 1000
        
        return word_count, latency_ms, cache_latency_ms
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0, 0, 0

def plot_metrics(latencies):
    x_labels = [pair[0] for pair in latencies]
    normal_latencies = [pair[1] for pair in latencies]
    cache_latencies = [pair[2] for pair in latencies]
    
    x = np.arange(len(x_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width/2, normal_latencies, width, label='Normal Latency')
    bars2 = ax.bar(x + width/2, cache_latencies, width, label='Cache Latency')

    ax.set_xlabel("Keyword-Filename Pair")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_title("Normal Latency vs Cache Latency (ms) for Keyword-Filename Pairs")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45)
    ax.legend()

    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()

    plt.savefig("/output/latency_plot.png")
    print("Plot saved as /output/latency_plot.png")

def plot_count(counts):
    x_labels = [pair[0] for pair in counts]
    count_values = [pair[1] for pair in counts]
    
    x = np.arange(len(x_labels))  # the label locations

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(x, count_values, width=0.5, color='green')

    ax.set_xlabel("Keyword-Filename Pair")
    ax.set_ylabel("Word Count")
    ax.set_title("Word Count for Each Keyword-Filename Pair")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()

    plt.savefig("/output/count.png")
    print("Plot saved as /output/count.png")

if __name__ == "__main__":
    conn = rpyc.connect("wordcount_server_1", 18812)
    print("Connection successful!")
    
    num_pairs = int(input("Enter the number of keyword-filename pairs: "))
    
    keyword_filename_pairs = []

    for _ in range(num_pairs):
        keyword = input("Enter the keyword: ")
        filename = input("Enter the filename: ")
        keyword_filename_pairs.append((filename, keyword))
    
    latencies = []
    counts = []
    
    for filename, keyword in keyword_filename_pairs:
        word_count, latency, cache_latency = get_word_count(conn, filename, keyword)
        
        print(f"The keyword '{keyword}' appears {word_count} times in {filename}.")
        print(f"First request latency: {latency:.4f} ms")  # Show more decimal places for accuracy
        print(f"Cache hit latency: {cache_latency:.4f} ms")
        
        latencies.append((f"{keyword}-{filename}", latency, cache_latency))
        counts.append((f"{keyword}-{filename}", word_count))
        
        conn.root.clear_cache()
    
    plot_metrics(latencies)
    
    plot_count(counts)