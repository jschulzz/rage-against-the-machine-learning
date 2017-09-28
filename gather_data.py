import sys
import spotipy
import spotipy.util as util

settings_file = open("settings.json").read()
settings = json.loads(settings_file)["settings"]
id = settings["id"]
secret = settings["secret"]

token = util.prompt_for_user_token(username='john_schulz', client_id=id, client_secret=secret, redirect_uri="https://localhost/", scope="user-top-read")
sp = spotipy.Spotify(auth=token)

genre = "rap"
l = 50
a_file = open("[" + genre + "]artists.txt", 'w', encoding='UTF-8')
a_short = open("[" + genre + "]artists_small.txt", 'w', encoding='UTF-8')
t_file = open("[" + genre + "]tracks.txt", 'w', encoding='UTF-8')
t_short = open("[" + genre + "]tracks_small.txt", 'w', encoding='UTF-8')
for i in range(0, 100):
    results = sp.search(q='genre:"' + genre + '"', type='track', limit=l, offset=i*l)
    # print(results)
    for track in results['tracks']['items']:
        artist = track['artists'][0]['name']
        title = track['name']
        print(title + " - " + artist)
        a_file.write(artist + '\n')
        t_file.write(title + '\n')
        if i < 5:
            a_short.write(artist + '\n')
            t_short.write(title + '\n')
a_file.close()
t_file.close()
