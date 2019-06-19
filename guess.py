import train
import settings
import numpy as np

if __name__ == "__main__":
    data = train.getData()
    all_genres, all_artists = train.makeSenseOfData(data)
    charDict = train.createCharDict(all_artists, settings.NULL_CHAR)
    m = train.createModel(settings.PADDING_LENGTH * len(charDict), len(all_genres))
    # m.build()?
    # print(m.summary())
    m.load_weights("weights-improvement-03-0.0152.hdf5")
    while True:
        artist = input("Artist Name: ")
        padded_name = artist.ljust(settings.PADDING_LENGTH, settings.NULL_CHAR)
        encoded_name = train.flattenList(train.encodeName(padded_name, charDict))
        # print(encoded_name)
        prediction = m.predict(np.asarray([encoded_name]))
        sorted_prediction = np.argsort(prediction)[0]
        print("max val {}".format(np.max(prediction)))
        for i in range(1, 4):
            genre_idx = sorted_prediction.tolist()[-i]
            print("Genre {}: {}".format(i, all_genres[genre_idx]))
            print("Confidence: {}".format(prediction[0][genre_idx]))



