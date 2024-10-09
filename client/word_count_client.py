import rpyc
import argparse

parser = argparse.ArgumentParser(description='Word Count Client')
parser.add_argument('keyword', type=str, help='Keyword to count in the text')
parser.add_argument('filename', type=str, help='Name of the text file') #make it identifier?

args = parser.parse_args()

def get_word_count(keyword):
    try:
        conn = rpyc.connect("wordcount_server_1", 18812)
        print("Connection successful!")
        word_count = conn.root.exposed_word_count(args.filename,args.keyword)
        return word_count
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0
    

if __name__ == "__main__":
    keyword= args.keyword
    word_count = get_word_count(keyword)
    print(f"The keyword '{keyword}' appears {word_count} times.")
