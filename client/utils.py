import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def server_warmup(conn):
    """
    Perform a dummy warm-up call to the server to reduce the delay in the first actual request.
    """
    print("Performing warm-up request...")
    conn.root.exposed_word_count("dummyfile", "dummykeyword")
    print("Warm-up request completed.\n")

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
                    xytext=(0, 3),
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
    
    x = np.arange(len(x_labels))

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
