import os
from sys import getsizeof
import json
import settings
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import metrics, optimizers
import numpy as np
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping


def encodeName(name, charDict):
    result = []
    # result.append(1/len(text))
    # result.append(1/len(text.split()))
    for letter in name:
        encoding = [0 for char in charDict]  # 0s for all characters
        encoding[charDict.index(letter)] = 1
        result.append(encoding)
    return result


def createCharDict(all_names, null_char):
    resulting_arr = []  # will look like ['a', 'b', 'c' ... ]
    for name in all_names:
        for letter in name:
            if letter not in resulting_arr:
                resulting_arr.append(letter)
    if null_char not in resulting_arr:
        resulting_arr.append(null_char)
    resulting_arr.sort(key=ord)
    return resulting_arr


def encodeGenre(all_genres, matching_genres):
    resulting_arr = [0 for g in all_genres]  # will look like ['a', 'b', 'c' ... ]
    for genre in matching_genres:
        resulting_arr[all_genres.index(genre)] = 1
    return resulting_arr


def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))


def clearOldNetworks():
    for file in os.listdir(os.curdir):
        if file.startswith("weights-improvement"):
            os.remove(file)


def getData():
    data_filename = settings.DATA_FILE
    data = {}
    with open(data_filename) as file:
        data = json.load(file)
    return data


def flattenList(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list

def makeSenseOfData(data):

    all_genres = list(set(flattenList(list(map(lambda x: x["genres"], data)))))
    all_genres.sort()

    all_artists = list(set(list(map(lambda x: x["artist_name"], data))))
    # all_artists.sort(key=len)
    # longest_name_len = len(all_artists[-1])
    all_artists.sort()

    return all_genres, all_artists



def transformData(data):

    null_char = settings.NULL_CHAR
    longest_name_len = settings.PADDING_LENGTH
    all_genres, all_artists = makeSenseOfData(data)

    charDict = createCharDict(all_artists, null_char)

    lookup_dict = {}

    for entry in data:
        artist = entry["artist_name"]
        genres = entry["genres"]
        if artist not in lookup_dict:
            lookup_dict[artist] = genres

    given_input = []
    expected_output = []

    print(len(all_genres), "genres recorded")
    print(len(all_artists), "artists recorded")

    for idx, artist in enumerate(all_artists):
        if idx % 1000 is 0:
            print("Artist #{}/{}".format(idx, len(all_artists)))
            print("Sitting at {} and {}".format(getsizeof(given_input), getsizeof(expected_output)))
        if idx > 4000:
            break
        padded_name = artist.ljust(longest_name_len, null_char)
        encoded_name = flattenList(encodeName(padded_name, charDict))
        matching_genres = lookup_dict[artist]
        encoded_genres = encodeGenre(all_genres, matching_genres)
        # print("{} - {}".format(artist, matching_genres))
        # sorted_prediction = np.argsort(encoded_genres)
        # for i in range(1, 4):
        #     print(sorted_prediction)
        #     print("Genre {}: {}".format(i, all_genres[sorted_prediction.tolist()[-i]]))
        given_input.append(encoded_name)
        expected_output.append(encoded_genres)

    print("Total inputs:", len(given_input))
    print("Total outputs:", len(expected_output))

    return given_input, expected_output


def createModel(name_length, output_length):
    model = Sequential()
    # model.add(Dropout(0.3))
    model.add(Dense(500, activation="relu", input_shape=(name_length,)))
    model.add(Dropout(0.6))
    model.add(Dense(1000, activation="relu"))
    model.add(Dropout(0.6))
    model.add(Dense(output_length, activation="sigmoid"))
    model.compile(
        optimizer=optimizers.Adam(lr=0.05),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    clearOldNetworks()
    data = getData()
    given_input, expected_output = transformData(data)
    print(len(given_input))
    print(len(given_input[0]))
    print(len(expected_output))
    print(len(expected_output[0]))

    model = createModel(len(given_input[0]), len(expected_output[0]))
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor="loss", verbose=1, save_best_only=True, mode="min"
    )
    stopper = EarlyStopping(
        monitor="loss", min_delta=0.0005, patience=30, mode="auto"
    )
    callbacks_list = [checkpoint, stopper]
    print("Fitting Now")
    model.fit(
        np.asarray(given_input),
        np.asarray(expected_output),
        epochs=100,
        batch_size=64,
        callbacks=callbacks_list,
        validation_split=0.2,
        shuffle=True,
    )
