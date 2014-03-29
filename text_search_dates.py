from text_search import *
import sys

def main():
    text_search = TextSearch(sys.argv[1])
    return text_search.get_date_values()

if __name__ == "__main__":
    dates = main()
    
    try:
        for date in dates:
            print date
    except KeyError:
        print ''