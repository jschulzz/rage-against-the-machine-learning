import json
import spotipy
import spotipy.util as util

settings_file = open("My_settings.json").read()
settings = json.loads(settings_file)["settings"]
id = settings["id"]
secret = settings["secret"]

token = util.prompt_for_user_token(username='john_schulz', client_id=id, client_secret=secret, redirect_uri="https://localhost/", scope="user-top-read")
sp = spotipy.Spotify(auth=token)

def clean(data):
	return json.dumps(data, indent=4, sort_keys=True)

# genres = sp.recommendation_genre_seeds()
song_list = []

# for genre in genres["genres"]:
# 	genre_list = []
# 	genre_list.append(genre)
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
all_artists = []

for letter in alpha:
	LIMIT = 50
	for i in range(100):
		search_results = sp.search(q="*"+letter+"*", type="artist", limit=LIMIT, offset=(LIMIT * i))
		# print(clean(search_results))

		# recommendations = sp.recommendations(seed_genres=genre_list, limit=100)
		# albums = sp.new_releases(limit=(LIMIT), offset=(LIMIT * i))
		# print(json.dumps(recommendations, sort_keys=True, indent=2))
		# print()
		for artist in search_results["artists"]["items"]:
			# print(track["artists"][0]["name"], track["album"]["name"], track["popularity"])
			# saved_data = {
			# 	"track_name": track["name"],
			# 	"album_name": track["album"]["name"],
			# 	"artist_name": track["artists"][0]["name"],
			# 	"genre": genre
			# }
			# print(clean(artist))
			# for artist in album["artists"]:
			artist_name = artist["name"]
			if artist_name not in all_artists:
				all_artists.append(artist_name)
				artist_id = artist["id"]
				genres = artist["genres"]
				if len(genres) > 0:
					# print(clean(artist))
					print("[{}] - {}".format(i, artist_name))
					saved_data = {
						"artist_name": artist_name,
						"genres": genres
					}
					song_list.append(saved_data)
		# print("[", i, "] saved a record of", genre)
print("writing Data")
with open("song_data.json", 'w', encoding='UTF-8') as song_file:
	json.dump(song_list, song_file, indent=4)
# genre = "rap"
# l = 50
# a_file = open("[" + genre + "]artists.txt", 'w', encoding='UTF-8')
# a_short = open("[" + genre + "]artists_small.txt", 'w', encoding='UTF-8')
# t_file = open("[" + genre + "]tracks.txt", 'w', encoding='UTF-8')
# t_short = open("[" + genre + "]tracks_small.txt", 'w', encoding='UTF-8')
# for i in range(0, 100):
#     results = sp.search(q='genre:"' + genre + '"', type='track', limit=l, offset=i*l)
#     # print(results)
#     for track in results['tracks']['items']:
#         artist = track['artists'][0]['name']
#         title = track['name']
#         print(title + " - " + artist)
#         a_file.write(artist + '\n')
#         t_file.write(title + '\n')
#         if i < 5:
#             a_short.write(artist + '\n')
#             t_short.write(title + '\n')

# a_file.close()
# t_file.close()
