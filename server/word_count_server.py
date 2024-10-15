import os
import rpyc
import redis

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

class WordCountService(rpyc.Service):
    def exposed_word_count(self, fileName, keyword):
        cache_key = f"{fileName}:{keyword}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            print(f"Cache hit for {cache_key}")
            return int(cached_result)
        
        print(f"Cache miss for {cache_key}")
        
        try:
            with open(f"/server/{fileName}.txt", "r") as file:
                text = file.read()
        except FileNotFoundError:
            return f"Text file {fileName} not found"

        count = text.lower().split().count(keyword.lower())
        
        redis_client.set(cache_key, count)
        
        return count

    def exposed_clear_cache(self):
        # Clear the entire Redis cache
        redis_client.flushdb()
        print("Cache cleared after batch request")

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(WordCountService, port=18812, hostname='0.0.0.0')
    print("Server started on port 18812")
    server.start()
