import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def server_warmup(conn):
    print("Performing warm-up request...")
    conn.root.exposed_word_count("dummyfile", "dummykeyword")
    print("Warm-up request completed.\n")

def plot_metrics(latencies):
    xLabel = [pair[0] for pair in latencies]
    normal_latencies = [pair[1] for pair in latencies]
    cache_latencies = [pair[2] for pair in latencies]

    x = np.arange(len(xLabel))
    width = 0.35
    fig, axis = plt.subplots(figsize=(10, 6))
    barNormal = axis.bar(x - width/2, normal_latencies, width, label='Normal Latency')
    barCache = axis.bar(x + width/2, cache_latencies, width, label='Cache Latency')
    axis.set_xlabel("Keyword-Filename Pair")
    axis.set_ylabel("Latency (milliseconds)")
    axis.set_title("Normal Latency vs Cache Latency (ms) for Keyword-Filename Pairs")
    axis.set_xticks(x)
    axis.set_xticklabels(xLabel, rotation=45)
    axis.legend()

    for bar in barNormal:
        height = bar.get_height()
        axis.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    for bar in barCache:
        height = bar.get_height()
        axis.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("/output/latency_plot.png")
    print("Plot saved as /output/latency_plot.png")

def plot_count(counts):
    xLabel = [pair[0] for pair in counts]
    count_values = [pair[1] for pair in counts]
    x = np.arange(len(xLabel))
    fig, axis = plt.subplots(figsize=(10, 6))
    bars = axis.bar(x, count_values, width=0.5, color='green')
    axis.set_xlabel("Keyword-Filename Pair")
    axis.set_ylabel("Word Count")
    axis.set_title("Word Count for Each Keyword-Filename Pair")
    axis.set_xticks(x)
    axis.set_xticklabels(xLabel, rotation=45)

    for bar in bars:
        height = bar.get_height()
        axis.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("/output/count.png")
    print("Plot saved as /output/count.png")
