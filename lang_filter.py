import pandas
import requests
import string

# The following link contains a text file with the 20,000
# most frequent words in english, one in each line.
DICTIONARY_URL = 'https://raw.githubusercontent.com/first20hours/' \
                 'google-10000-english/master/20k.txt'
PATH = r"twitter_human_bots_dataset1.csv"
FILTER_COLUMN_NAME = 'description'
PRINTABLES_SET = set(string.printable)

def is_english_printable(word):
    return PRINTABLES_SET >= set(word)

def prepare_dictionary(url):
    return set(requests.get(url).text.splitlines())

DICTIONARY = prepare_dictionary(DICTIONARY_URL)
df = pandas.read_csv(PATH, encoding='ISO-8859-1')
df = df[df[FILTER_COLUMN_NAME].map(is_english_printable) &
        df[FILTER_COLUMN_NAME].map(str.lower).isin(DICTIONARY)]
