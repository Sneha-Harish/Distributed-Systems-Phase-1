import rpyc

def get_word_count(keyword):
    # conn = rpyc.connect("localhost", 18812) #initially working with one server
    
    # # Call the server's exposed word_count method
    # word_count = conn.root.word_count(keyword)
    # return word_count
    return 0

if __name__ == "__main__":
    # keyword = input("Enter the keyword to count: ")
    keyword="try"
    word_count = get_word_count(keyword)
    print(f"The keyword '{keyword}' appears {word_count} times.")
