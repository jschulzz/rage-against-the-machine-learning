import os
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# load ascii text and covert to lowercase
for file in os.listdir(os.curdir):
	if file.startswith("weights-improvement"):
		os.remove(file)
settings_file = open("settings.json").read()
settings = json.loads(settings_file)["settings"]
filename = settings["training_file"]
null_char = settings["null_char"]
artists = open(filename).read().lower().split("\n")
unique_chars = sorted(list(set(open(filename).read().lower().replace("\n", ""))))
unique_chars.append(null_char)

# create mapping of unique chars to integers
max_length = (len(max(artists, key=len)))
char_to_int = dict((c, i) for i, c in enumerate(unique_chars))
# summarize the loaded data

for i, artist in enumerate(artists):
	while len(artist) < max_length:
		artist += null_char
	artists[i] = artist

artists_matrix = []
n_chars = len(artists)
n_vocab = len(unique_chars)

for artist in artists:
	m = [[0 for x in range(n_vocab)] for y in range(max_length)]
	for i in range(len(artist)):
		m[i][char_to_int[artist[i]]] = 1
	artists_matrix.append(m)

print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)
# prepare the dataset of input to output pairs encoded as integers
sequence_size = settings["sequence_size"]
dataX = []
dataY = []
for artist in artists_matrix:
	for i in range(0, len(artist) - sequence_size):
		seq_in = artist[i:i+sequence_size]
		seq_out = artist[i+sequence_size]
		dataX.append(seq_in)
		dataY.append(seq_out)
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(sequence_size, len(unique_chars)), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(len(dataY[1]), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
print("About to fit")
model.fit(dataX, dataY, epochs=50, batch_size=64, callbacks=callbacks_list)
