import settings
import json
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize

def getData():
    data_filename = settings.DATA_FILE
    data = {}
    with open(data_filename) as file:
        data = json.load(file)
    return data


def makeSenseOfData(data):
    all_genres = list(set(flattenList(list(map(lambda x: x["genres"], data)))))
    all_genres.sort()
    all_artists = list(set(list(map(lambda x: x["artist_name"].lower(), data))))
    # all_artists.sort(key=len)
    # longest_name_len = len(all_artists[-1])
    all_artists.sort()
    return all_genres, all_artists

def encodeName(name, wordBag):
    encoding = [0 for word in wordBag]  # 0s for all characters
    # result.append(1/len(text))
    # result.append(1/len(text.split()))
    name = name.lower()
    tokens = word_tokenize(name)
    for t in tokens:
        root = stem(t)
        encoding[wordBag.index(root)] = 1
    return encoding


def createWordBag(all_names):
    resulting_arr = set()  # will look like ['a', 'b', 'c' ... ]
    for name in all_names:
        name = name.lower()
        tokens = word_tokenize(name)
        for t in tokens:
            root = stem(t)
            resulting_arr.add(root)
    # if null_char not in resulting_arr:
    #     resulting_arr.add(null_char)
    return list(resulting_arr)

    # TODO: What if we indexed the words instead of characters? I.E. bag of words


def encodeGenre(all_genres, matching_genres):
    resulting_arr = [0 for g in all_genres]  # will look like ['a', 'b', 'c' ... ]
    for genre in matching_genres:
        resulting_arr[all_genres.index(genre)] = 1
    return resulting_arr

def flattenList(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list