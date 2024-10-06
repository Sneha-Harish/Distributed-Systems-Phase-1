import os
import rpyc
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class WordCountService(rpyc.Service):
    def exposed_word_count(self, keyword):
        print("Counting occurrences of:", keyword)
        # Placeholder for actual word count logic
        return 0  # Replace with actual count

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(WordCountService, port=18812)
    print("Server started on port 18812")
    server.start()

