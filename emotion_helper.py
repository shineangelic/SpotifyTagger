import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import json
import math as mt
import time
import matplotlib.pyplot as plt
'''Forked https://github.com/brentvollebregt/Lucy-In-The-Sky-With-Emotion'''

def chunks(l, n):
    # Thanks to http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

with open('settings.json') as data_file:
    settings = json.load(data_file)

client_credentials_manager = SpotifyClientCredentials(client_id=settings['spotify']['client_id'], client_secret=settings['spotify']['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

def get_artist_genres(urn:str):
    genres = []
    results = sp.search(q='artist:' + urn, type='artist')
    items = results['artists']
    for it in items['items']:
        for genre in it['genres']:
            genres.append(genre)
    print(genres)
    return genres

def import_from_dir(directory):
    """
    Args:
        directory: string of directory to be searched
    Returns: Lists of dictionaries with mp3 file locations in 'file_location' -> [{'file_location': 'c://a.mp3'},{'file_location': 'c://b.mp3'}] (each dictionary will be a dictionary of a song)
    """
    songs = []
    import os
    for root, dirs, files in os.walk(directory, topdown=True):
        for name in files:
            if name.endswith(".mp3"):
                songs.append({'file_location': os.path.join(root, name)})
    return songs

def get_tags(song):
    """
    Args:
        song: dictionary of song
    Returns: dictionary of song with 'title', 'artist' and 'album' added
    """
    audio = ID3(song['file_location'])
     
    song['title'] = audio['TIT2'].text[0] 
    song['artist'] = audio['TPE1'].text[0]
    song['album'] = audio['TALB'].text[0]
    if 'TPE2' in audio:
        song['album artist'] = audio['TPE2'].text[0]
    return song

def get_uri(song):
    """
    Args:
        song: dictionary of song
    Returns: dictionary of song with 'spotify_uri' added
    """
    srchk = 'track:' +song['title'] + ' '+'artist:' + song['artist']
    if 'album artist' in song:
        srchk += ' '+'artist:' + song['album artist']
    else:
        srchk += ' '+'artist:' + song['artist']
    #if song['album']:
    #    srchk += ' '+'album:' + song['album']
    result = sp.search(srchk)
    for i in result['tracks']['items']:
        if (i['artists'][0]['name'] == song['artist']) and (i['name'] == song['title']):
            song['uri'] = i['uri']
            break
    else:
        try:
            song['uri'] = result['tracks']['items'][0]['uri']
        except:
            return None
    return song

def int_index_to_uri_index(songs):
    converted = {}
    for i in songs:
        converted[i['uri']] = i
    return converted

def get_spotify_data(songs):
    """
    Args:
        songs: list of dictionaries of songs indexed by uri
    Returns: list of dictionaries of songs with 'energy', 'valence' and 'tempo' added
    """
    indexs = [i for i in songs]
    indexs_chunked = chunks(indexs, 50)
    for chunk in indexs_chunked:
        features = sp.audio_features(chunk)
        for song in features:
            if song != None:
                songs[song['uri']]['energy'] = song['energy']
                songs[song['uri']]['valence'] = song['valence']
                songs[song['uri']]['tempo'] = song['tempo']
                songs[song['uri']]['danceability'] = song['danceability']
                songs[song['uri']]['speechiness'] = song['speechiness']
                songs[song['uri']]['acousticness'] = song['acousticness']
                songs[song['uri']]['instrumentalness'] = song['instrumentalness']
                songs[song['uri']]['liveness'] = song['liveness']
                songs[song['uri']]['mode'] = song['mode']
                songs[song['uri']]['loudness'] = song['loudness']
                songs[song['uri']]['url'] = song['analysis_url']
                songs[song['uri']]['uri'] = song['uri']
        time.sleep(0.2)
        print(song['uri'])
    return songs

def get_length_of_file(location):
    """
    Args:
        location: location of a MP3
    Returns: float of MP3 length
    """
    audio = MP3(location)
    return audio.info.length


def generatePlot(songs):
    """
    Args:
        songs: The dictionary of songs that the user has imported
    Returns: Draws a plot that the user can see their songs data on 
            Colours the points based on their value 
    """
    energy = []
    valence = []
    colour = []

    for song in songs:
            energy += [songs[song]['energy']]
            valence += [songs[song]['valence']]
            colour += [mt.sqrt(songs[song]['energy']**2 + songs[song]['valence']**2)]
    plt.scatter(valence,energy,c=colour)
    plt.xlabel('Valence')
    plt.ylabel('Energy')
    plt.axis([0,1,0,1])
    plt.show()
