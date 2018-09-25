import os
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import metrics, optimizers
import numpy as np
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
# from keras.utils import np_utils

def toASCII(text):
	result = []
	result.append(1/len(text))
	result.append(1/len(text.split()))
	for letter in text:
		result.append(ord(letter) / 256)
	return result


def mode(array):
	most = max(list(map(array.count, array)))
	return list(set(filter(lambda x: array.count(x) == most, array)))

# load ascii text and covert to lowercase
for file in os.listdir(os.curdir):
	if file.startswith("weights-improvement"):
		os.remove(file)
settings_file = open("My_settings.json").read()
settings = json.loads(settings_file)["settings"]
filename = settings["training_file"]
null_char = settings["null_char"]

data = {}
with open(filename) as file:
	data = json.load(file)

genre_list = []
# for record in data:
# 	genre_list += record["genres"]
# genre_list.sort()
artist_list = list(map(lambda x: x["artist_name"], data))
final_dict = {}

for entry in data:
	# print(entry)
	artist = entry["artist_name"]
	genres = entry["genres"]
	if len(genres) > 2:
		genre_list += genres
		try:
			final_dict[artist] += genres
		except KeyError:
			final_dict[artist] = genres
genre_list = list(set(genre_list))
genre_list.sort()
print(len(genre_list), "genres recorded")
	# final_dict[artist] = list(set(final_dict[artist]))
	# print(final_dict[artist])
print("final_dict made")
# print(final_dict)
# for entry in final_dict:
# 	print(entry)
# artist_list = list(map(lambda x: x["track_name"], data))
# artist_list = list(map(lambda x: x["album_name"], data))
ASCII_list = list(map(lambda x: toASCII(x), final_dict.keys()))
print("Total Data points:", len(ASCII_list))
output_list = []
for artist in final_dict:
	# print(final_dict[artist])
	output = [0] * len(genre_list)
	output[genre_list.index(mode(final_dict[artist])[0])] = 1
	output_list.append(output)



# print(output_list)

max_size = len(max(artist_list, key=len))
print("Made output map. Max Size: {}".format(max_size))
for ascii in ASCII_list:
	ascii += [0.0] * (max_size - len(ascii))

# print(ASCII_list)

print("Data Organized. Building Model")


model = Sequential()
model.add(Dropout(0.3))
model.add(Dense(500, activation='relu', input_shape=(max_size,)))
model.add(Dropout(0.6))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(len(output_list[0]), activation='sigmoid'))
model.compile(optimizer=optimizers.Adam(lr=0.05),
			  loss='binary_crossentropy',
			  metrics=['accuracy'])

filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.8, patience=10, mode='auto', min_delta=0.001, cooldown=2, min_lr=0.00001)
stopper = EarlyStopping(monitor='val_loss', min_delta=0.0005, patience=30, mode='auto')
callbacks_list = [checkpoint, reduce, stopper]
print("Fitting Now")
model.fit(np.asarray(ASCII_list), np.asarray(output_list), epochs=10000, batch_size=3000, callbacks=callbacks_list, validation_split=0.2, shuffle=True)
# print(artist_list)
# artists = open(filename).read().lower().split("\n")
# unique_chars = sorted(list(set(open(filename).read().lower().replace("\n", ""))))
# unique_chars.append(null_char)
#
# # create mapping of unique chars to integers
# max_length = (len(max(artists, key=len)))
# char_to_int = dict((c, i) for i, c in enumerate(unique_chars))
# # summarize the loaded data
#
# for i, artist in enumerate(artists):
# 	while len(artist) < max_length:
# 		artist += null_char
# 	artists[i] = artist
#
# artists_matrix = []
# n_chars = len(artists)
# n_vocab = len(unique_chars)
#
# for artist in artists:
# 	m = [[0 for x in range(n_vocab)] for y in range(max_length)]
# 	for i in range(len(artist)):
# 		m[i][char_to_int[artist[i]]] = 1
# 	artists_matrix.append(m)
#
# print("Total Characters: ", n_chars)
# print("Total Vocab: ", n_vocab)
# # prepare the dataset of input to output pairs encoded as integers
# sequence_size = settings["sequence_size"]
# dataX = []
# dataY = []
# for artist in artists_matrix:
# 	for i in range(0, len(artist) - sequence_size):
# 		seq_in = artist[i:i+sequence_size]
# 		seq_out = artist[i+sequence_size]
# 		dataX.append(seq_in)
# 		dataY.append(seq_out)
# n_patterns = len(dataX)
# print("Total Patterns: ", n_patterns)
# # define the LSTM model
# model = Sequential()
# model.add(LSTM(256, input_shape=(sequence_size, len(unique_chars)), return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(256))
# model.add(Dropout(0.2))
# model.add(Dense(len(dataY[1]), activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adam')
# # define the checkpoint
# filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
# callbacks_list = [checkpoint]
# # fit the model
# print("About to fit")
# model.fit(dataX, dataY, epochs=50, batch_size=64, callbacks=callbacks_list)
