from text_search import *
import sys

def main():
    text_search = TextSearch(sys.argv[1])
    return text_search.get_entity_names()

if __name__ == "__main__":
    entity = main()

    try:
        for word in entity:
            print word
    except KeyError:
        print ''