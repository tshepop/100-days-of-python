import requests
from bs4 import BeautifulSoup
import config

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET

# scraping or crawling the billboard hot 100

print("billboard hot 100 songs".upper().center(86, "-"))
songs_year = input("Which year do you want to travel to? Type date in this format(YYYY-MM-DD): ")
year = songs_year.split("-")[0]
month = songs_year.split("-")[1]
day = songs_year.split("-")[2]

url = f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}"

req = requests.get(url=url)
response = req.text

soup = BeautifulSoup(response, "html.parser")
#print(soup.prettify())

#song_title_list = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
song_title_list = soup.find_all("h3", class_="a-no-trucate")
#print(song_title_list)

song_list = []

for idx, song in enumerate(song_title_list, start=1):
    #print(idx, song.getText())
    titles = song.getText().strip()
    song_list.append(titles)
    #print(f"{str(idx)}. {titles}\n")

# spotify library and retrieve spotify song data

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope=scope))

user_id = sp.me()["id"]

# I created the text file after, it was not created running after the script
# comment the following code, adds no value to the program
# with open(r".cache", "r") as file, open("token.txt", "w") as file2:
#     for line in file:
#         file2.write(line)

#songs_year = input("Which year do you want to travel to? Type date in this format(YYYY-MM-DD): ")
#year = songs_year.split("-")[0]

# results = []
# with open("billboard-songs-100.txt", "r") as file:
#     songs = file.readlines()
#     #print(songs)
    
#     for title in songs:
#         track = title.strip()
#         results.append(track)

#print(results)

#counter = 0
# for name in results:
#     try:
#         track_name = sp.searchf(q=f"track:{name} year:{year}", limit=1, type="track")

#         for track in track_name['tracks']['items'][0]:
#             print(track['uri'])
#             counter += 1
#         print(counter)
#     except IndexError:
#         print("The song cannot be found!")

uri_list = []
for idx, name in enumerate(song_list):
    track_name = sp.search(q=f"track:{name} year:{year}", limit=1, type="track")
    try:
        track = track_name["tracks"]["items"][0]
        uri_list.append(track["uri"])
        print(str(idx+1), track["uri"])
    except IndexError:
        print("The song is not available on Spotify.")

# create playlist
playlist = sp.user_playlist_create(user_id, f"{year} Billboard 100", public=False, collaborative=False, description="Go down the memory lane, bring the favorite oldies to the now.")

# add tracks/songs to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)

