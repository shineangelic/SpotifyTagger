import os
import warnings

import eyed3
import emotion_helper
#from eyed3 import Mp3AudioFile

warnings.simplefilter("ignore")

ROOT_DIR = "E:\\Musica\\"
   
def parse_Dir(direct:str) -> int:
    '''Parsa e processa una dir'''
    done=0
    #totsize = 0
    directory = direct

    totalfiles = emotion_helper.import_from_dir(directory)

    if len(totalfiles) == 0:
        print('SKIPPING import_from_dir NOTHING FOUND', direct)
        return 0
    
    print("Searching tags for a total of mp3: ", str(len(totalfiles)))
    tagged_totalfiles = []
    
    for file in totalfiles:
        try:
            tagged_totalfiles.append(emotion_helper.get_tags(file))
        except Exception as e:
            print ('emotion_helper.get_tags Error: '+ str(e))

    if len(tagged_totalfiles) == 0:
        print('SKIPPING, NO TAG FOUND', direct)
        return 0

    uried_files = _get_spotify_uris(tagged_totalfiles)           
    uried_index = emotion_helper.int_index_to_uri_index(uried_files)

    print("Retrieving spotify data for found entries:", len(uried_index))
    tagged_files = emotion_helper.get_spotify_data(uried_index) 

    for daaggiornare, audiof in tagged_files.items():
        print('UPDATING ', daaggiornare)
        try:
            _process_audiofile(audiof)
            done+=1
        except Exception as e:
            print ('Error: '+ str(e))
    print('END. DONE: ', done)
    print('END. NOT DONE: ', len(totalfiles) - done)
    return done

def _get_spotify_uris(tagged_totalfiles:list):
    '''Uses emotion_helper.get_uri and search songs loop'''
    print("Getting spotify URI for a total of mp3: ", str(len(tagged_totalfiles)))     
    genres = []  
    uri_totalfiles = []
    xlibstr = ''

    for ii,file in enumerate(tagged_totalfiles):
        # print ("\r" + str(round((count/len(tagged_totalfiles))*100, 2)) + "%", end='')
        tmp_song = emotion_helper.get_uri(file)
        print('SEARCH ',ii, file)

        if 'uri' in tmp_song:
            if len(genres) == 0:
                try:
                    artistk = tmp_song['album artist']
                except Exception:
                    artistk = tmp_song['artist']
                genres = emotion_helper.get_artist_genres(artistk)
                for gen in genres:
                    xlibstr += gen + ';'

            tmp_song['genres'] = xlibstr
            uri_totalfiles.append(tmp_song)
    return uri_totalfiles

def _process_audiofile(km):
    '''Saves found data inside SPTY_* TAGS'''
    audiofile = eyed3.load(km['file_location'])
    newg = str(km['genres'])
    audiofile.tag.user_text_frames.set(newg,"SPTY_GENRE" )
    audiofile.tag.user_text_frames.set(str(km['tempo']),"SPTY_TEMPO" )
    audiofile.tag.user_text_frames.set(str(km['mode']),"SPTY_MODE" )
    audiofile.tag.user_text_frames.set(str(km['uri']),"SPTY_URI" )

    valence = int(km['valence'] * 100)
    audiofile.tag.user_text_frames.set(str(valence),"SPTY_VALENCE" )

    #acousticness = int(km['acousticness'] * 100)
    #audiofile.tag.user_text_frames.set(str(acousticness),"SPTY_ACOUSTICNESS" )

    energy = int(km['energy'] * 100)
    audiofile.tag.user_text_frames.set(str(energy),"SPTY_ENERGY" )

    liveness = int(km['liveness'] * 100)
    audiofile.tag.user_text_frames.set(str(liveness),"SPTY_LIVENESS" )

    danceability = int(km['danceability'] * 100)
    audiofile.tag.user_text_frames.set(str(danceability),"SPTY_DANCEABILITY" )

    instrumentalness = int(km['instrumentalness'] * 100)
    audiofile.tag.user_text_frames.set(str(instrumentalness),"SPTY_INSTRUMENTALNESS" )

    audiofile.tag.user_text_frames.set(str(km['loudness']),"SPTY_LOUDNESS" )

    audiofile.tag.save()

if __name__ == '__main__':
    res = 0
    diridx = 0
    for root, dirs, files in os.walk(ROOT_DIR, topdown=True):
        diridx += 1
        for i,name in enumerate(dirs):
            print(str(i)+"/"+str(len(dirs)) +" PROCESS: ", root+ '\\' +name)  
            res += parse_Dir(root+ '\\' +name)

