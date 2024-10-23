import rpyc
import time
from utils import server_warmup, plot_count, plot_metrics

def get_word_count(conn, filename, keyword):
    try:
        start_time = time.time()
        word_count = conn.root.exposed_word_count(filename, keyword)
        latency = time.time() - start_time
        
        cache_start_time = time.time()
        word_count_cache = conn.root.exposed_word_count(filename, keyword)
        cache_latency = time.time() - cache_start_time

        latency_ms = latency * 1000
        cache_latency_ms = cache_latency * 1000
        return word_count, latency_ms, cache_latency_ms

    except ConnectionError as e:
        print(f"Connection failed: {e}")

    except Exception as e:
        print(f"An error occured: {e}")

    return 0,0,0

if __name__ == "__main__":
    conn = rpyc.connect("wordcount_server_1", 18812)
    print("Connection Successful!")

    server_warmup(conn)

    try:
        while True:
            num_pairs = int(input("Enter the number of keyword-filename pairs (or Ctrl+C to exit): "))
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
                print(f"First request latency: {latency:.4f} ms")
                print(f"Cache hit latency: {cache_latency:.4f} ms")
    
                latencies.append((f"{keyword}-{filename}", latency, cache_latency))
                counts.append((f"{keyword}-{filename}", word_count))

            conn.root.clear_cache()
            plot_metrics(latencies)
            plot_count(counts)

    except KeyboardInterrupt:
        print("\nBye!")