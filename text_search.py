from nltk.corpus import ieer
import nltk
from nltk_contrib import timex
import mx
import re

class TextSearch:

    def __init__(self, query_string):
        self.query_string = query_string
        sentences = nltk.sent_tokenize(query_string)
        self.tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        self.tagged_sentences = [nltk.pos_tag(sentence) for sentence in self.tokenized_sentences]
        self.binary_chunked_sentences = nltk.batch_ne_chunk(self.tagged_sentences, binary=True)
        self.multiclass_chunked_sentences = nltk.batch_ne_chunk(self.tagged_sentences, binary=False)
        self.temporal_sentences = timex.ground(timex.tag(query_string), mx.DateTime.gmt())


    def extract_entity_names(self, t):
        entity_names = []
        
        if hasattr(t, 'node') and t.node:
            if t.node == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(self.extract_entity_names(child))
                    
        return entity_names


    def get_entity_names(self):
        entity_names = []
        for tree in self.binary_chunked_sentences:
            # Print results per sentence
            # print extract_entity_names(tree)
            entity_names.extend(self.extract_entity_names(tree))
        return set(entity_names)


    def get_temporal_sentence(self):
        return self.temporal_sentences


    def get_dates(self):
        timex_regex = re.compile(r'<TIMEX2.*?</TIMEX2>', re.DOTALL)
        timex_found = timex_regex.findall(self.temporal_sentences)
        return timex_found


    def get_multiclass_chunks(self):
        return self.multiclass_chunked_sentences


    def get_binary_chunks(self):
        return self.binary_chunked_sentences



#   Testing
def demo():
    s = raw_input("Enter some text: ")

    text_search = TextSearch(s)

    print "Binary Tags:"
    print text_search.get_binary_chunks()

    print "Multiclass Tags:"
    print text_search.get_multiclass_chunks()

    print "Entity Names:"
    print text_search.get_entity_names()

    print "Sentence with Temporal Tags:"
    print text_search.get_temporal_sentence()

    print "Dates:"
    print text_search.get_dates()
