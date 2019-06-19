import json
import spotipy
import spotipy.util as util
import settings

# settings_file = open("My_settings.json").read()
# settings = json.loads(settings_file)["settings"]
spotify_id = settings.SPOTIFY_ID
spotify_secret = settings.SPOTIFY_SECRET

token = util.prompt_for_user_token(
    username="john_schulz",
    client_id=spotify_id,
    client_secret=spotify_secret,
    redirect_uri="https://localhost/",
    scope="user-top-read",
)
sp = spotipy.Spotify(auth=token)


def clean(data):
    return json.dumps(data, indent=4, sort_keys=True)



alpha = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
all_artists = []
song_list = []

for letter in alpha:
    LIMIT = 50
    for i in range(100):
        search_results = sp.search(
            q="*" + letter + "*", type="artist", limit=LIMIT, offset=(LIMIT * i)
        )
        print("BATCH #{}".format(i))
        for artist in search_results["artists"]["items"]:
            artist_name = artist["name"]
            if artist_name not in all_artists:
                all_artists.append(artist_name)
                artist_id = artist["id"]
                genres = artist["genres"]
                if len(genres) > 0:
                    saved_data = {"artist_name": artist_name, "genres": genres}
                    song_list.append(saved_data)
print("writing Data")
with open("song_data.json", "w", encoding="UTF-8") as song_file:
    json.dump(song_list, song_file, indent=4)
