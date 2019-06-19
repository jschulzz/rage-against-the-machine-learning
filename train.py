import os
from sys import getsizeof
import json
import settings
import data_manipulation
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import metrics, optimizers
import numpy as np
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping


def clearOldNetworks():
    for file in os.listdir(os.curdir):
        if file.startswith("weights-improvement"):
            os.remove(file)


def transformData(data):
    all_genres, all_artists = data_manipulation.makeSenseOfData(data)

    wordBag = data_manipulation.createWordBag(all_artists)
    lookup_dict = {}

    for entry in data:
        artist = entry["artist_name"].lower()
        genres = entry["genres"]
        if artist not in lookup_dict:
            lookup_dict[artist] = genres

    given_input = []
    expected_output = []

    print(len(all_genres), "genres recorded")
    print(len(all_artists), "artists recorded")
    print(len(wordBag), "unique words")

    for idx, artist in enumerate(all_artists):
        if idx % 1000 is 0:
            print("Artist #{}/{}".format(idx, len(all_artists)))
            print(
                "Sitting at {} and {}".format(
                    getsizeof(given_input), getsizeof(expected_output)
                )
            )
        if idx > 4000:
            break
        # name = artist.lower()
        # padded_name = artist.ljust(longest_name_len, null_char)
        encoded_name = data_manipulation.encodeName(artist, wordBag)
        matching_genres = lookup_dict[artist]
        encoded_genres = data_manipulation.encodeGenre(all_genres, matching_genres)
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
    model.add(Dense(1000, activation="relu", input_shape=(name_length,)))
    # model.add(Dropout(0.2))
    model.add(Dense(500, activation="relu"))
    # model.add(Dropout(0.2))
    model.add(Dense(output_length, activation="sigmoid"))
    model.compile(
        optimizer=optimizers.Adam(lr=0.05),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    clearOldNetworks()
    data = data_manipulation.getData()
    given_input, expected_output = data_manipulation.transformData(data)

    model = createModel(len(given_input[0]), len(expected_output[0]))
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor="loss", verbose=1, save_best_only=True, mode="min"
    )
    stopper = EarlyStopping(monitor="loss", min_delta=0.0005, patience=30, mode="auto")
    callbacks_list = [checkpoint, stopper]
    print("Fitting Now")
    model.fit(
        np.asarray(given_input),
        np.asarray(expected_output),
        epochs=100,
        batch_size=16,
        callbacks=callbacks_list,
        validation_split=0.2,
        shuffle=True,
    )
