import os
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import metrics, optimizers
import numpy as np
# from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
# from keras.utils import np_utils

def toASCII(text):
	result = []
	result.append(1/len(text))
	result.append(1/len(text.split()))
	for letter in text:
		result.append(ord(letter) / 256)
	return result

# load ascii text and covert to lowercase
settings_file = open("My_settings.json").read()
settings = json.loads(settings_file)["settings"]
filename = settings["training_file"]
null_char = settings["null_char"]
weights_filename = "weights-improvement-01-0.1944.hdf5"

data = {}
with open(filename) as file:
	data = json.load(file)

genre_list = []
for entry in data:
	genres = entry["genres"]
	if len(genres) > 2:
		genre_list += genres
genre_list = list(set(genre_list))
genre_list.sort()
artist_list = list(map(lambda x: x["artist_name"], data))
# artist_list = list(map(lambda x: x["track_name"], data))
# artist_list = list(map(lambda x: x["album_name"], data))
# each_genre_list = list(map(lambda x: x["genre"], data))
output_list = []

max_size = len(max(artist_list, key=len))


model = Sequential()
model.add(Dropout(0.3))
model.add(Dense(500, activation='relu', input_shape=(max_size,)))
model.add(Dropout(0.6))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(len(genre_list), activation='sigmoid'))
model.compile(optimizer=optimizers.Adam(lr=0.05),
			  loss='binary_crossentropy',
			  metrics=['accuracy'])


while 1:
	name = input("Artist Name")
	ascii = toASCII(name)
	ascii += [0.0] * (max_size - len(ascii))
	prediction = model.predict(np.expand_dims(ascii, axis=0))
	ind = np.argpartition(np.asarray(prediction), -4)[-4:]
	print(ind)
	# idx = np.argmax(prediction)
	a = np.asarray(genre_list)
	print(a[ind])



# artists = open(filename).read().lower().split("\n")
# unique_chars = sorted(list(set(open(filename).read().lower().replace("\n", ""))))
# unique_chars.append(null_char)
#
# # create mapping of unique chars to integers
# max_length = (len(max(artists, key=len)))
# char_to_int = dict((c, i) for i, c in enumerate(unique_chars))
# int_to_char = dict((i, c) for i, c in enumerate(unique_chars))
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
# # print(artists)
# print("Total Characters: ", n_chars)
# print("Total Vocab: ", n_vocab)
# # prepare the dataset of input to output pairs encoded as integers
# sequence_size = settings["sequence_size"]
# dataX = []
# dataY = []
# for artist in artists_matrix:
# 	for i in range(0, len(artist) - sequence_size):
# 		seq_in = artist[i:i + sequence_size]
# 		seq_out = artist[i + sequence_size]
# 		dataX.append(seq_in)
# 		dataY.append(seq_out)
# n_patterns = len(dataX)
# # print(dataX[0])
# print("Total Patterns: ", n_patterns)
# # define the LSTM model
# model = Sequential()
# model.add(LSTM(256, input_shape=(sequence_size, len(unique_chars)), return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(256))
# model.add(Dropout(0.2))
# model.add(Dense(len(dataY[1]), activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adam')
# # load the network weights
#
# model.load_weights(weights_filename)
# model.compile(loss='categorical_crossentropy', optimizer='adam')
#
#
# # pick a random seed
# def getPatternFromText(t):
# 	m = [[0 for x in range(n_vocab)] for y in range(sequence_size)]
# 	for i in range(len(m)):
# 		m[i][char_to_int[t[i]]] = 1
# 	# print(t[i])
# 	return m
#
#
# def getPatternText(p):
# 	return ''.join([int_to_char[value.index(1)] for value in p])
#
#
# def genPattern():
# 	start = numpy.random.randint(0, len(artists) - 1)
# 	a = artists[start]
# 	p = getPatternFromText(a)
# 	p_text = getPatternText(p)
#
# 	while p_text[len(p_text) - 1] == null_char:
# 		start = numpy.random.randint(0, len(artists) - 1)
# 		a = artists[start]
# 		p = getPatternFromText(a)
# 		p_text = getPatternText(p)
# 	return p
#
#
# pattern = genPattern()
# pattern_ints = [value.index(1) for value in pattern]
# pattern_text = getPatternText(pattern)
# # print(pattern)
# print("Seed:")
# print("\"", ''.join(pattern_text), "\"")
#
# out_file = open(filename[0:len(filename) - 4] + "_results.txt", 'w', encoding="UTF-8")
# out_file.write("|" + pattern_text + "|")
# # generate characters
# for i in range(2000):
# 	prediction = model.predict(numpy.expand_dims(pattern, axis=0), verbose=0)
# 	index = numpy.argmax(prediction)
# 	result = int_to_char[index]
# 	print(result)
# 	if result != null_char:
# 		seq_in = [int_to_char[value.index(1)] for value in pattern]
# 		sys.stdout.write(result)
# 		out_file.write(result)
# 		temp = [0 for k in range(len(unique_chars))]
# 		temp[index] = 1
# 		pattern.append(temp)
# 		pattern = pattern[1:len(pattern)]
# 	else:
# 		print()
# 		pattern = genPattern()
# 		sys.stdout.write("|" + getPatternText(pattern) + "|")
# 		out_file.write("\n|" + getPatternText(pattern) + "|")
# seed = " "
# result = " "
# exit_seed = "    0"
# print("\n")
# out_file.write("\n-----USER ENTRIES-----")
# while seed != exit_seed:
# 	pattern = ""
# 	seed = ""
# 	result = ""
# 	full_title = ""
# 	while True:
# 		try:
# 			print("\n")
# 			original_seed = input("Enter a Seed [0 to exit]: ")
# 			seed = "      " + original_seed
# 			seed = seed[len(seed)-5:len(seed)]
# 			pattern = getPatternFromText(seed)
# 		except:
# 			print("I Guess some weird character? Try again")
# 			continue
# 		break
# 	if seed != exit_seed:
# 		sys.stdout.write("Result: " + original_seed)
# 		out_file.write("\n|" + seed + "|")
# 	full_title += seed
# 	while seed != exit_seed and result != null_char and len(full_title) < 100:
# 		seq_in = getPatternText(pattern)
# 		sys.stdout.write(result)
# 		out_file.write(result)
# 		full_title += result
# 		prediction = model.predict(numpy.expand_dims(pattern, axis=0), verbose=0)
# 		index = numpy.argmax(prediction)
# 		result = int_to_char[index]
#
# 		temp = [0 for k in range(len(unique_chars))]
# 		temp[index] = 1
# 		pattern.append(temp)
# 		pattern = pattern[1:len(pattern)]
#
# out_file.close()
# print("\nDone.")
