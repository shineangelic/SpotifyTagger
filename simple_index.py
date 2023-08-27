import sys 
import os
import emotion_helper

import eyed3
#from eyed3 import Mp3AudioFile


import warnings
warnings.simplefilter("ignore")
 

         
def parse_Dir(direct:str):
    '''Parsa e processa una dir'''
    done=0
    totsize = 0
    directory = direct

    totalfiles = emotion_helper.import_from_dir(directory)
    totsize = len(totalfiles)
    print("Getting spotify for a total of mp3: ", str(len(totalfiles)))
    tagged_totalfiles = []
    uri_totalfiles = []
    for file in totalfiles:
        try:
            tagged_totalfiles.append(emotion_helper.get_tags(file))
        except Exception as e:
            print ('Error: '+ str(e))

    print("Getting spotify URI for a total of mp3: ", str(len(tagged_totalfiles)))     
    genres = []  
    xlibstr = ''
    for i,file in enumerate(tagged_totalfiles):
        # print ("\r" + str(round((count/len(tagged_totalfiles))*100, 2)) + "%", end='')
        tmp = emotion_helper.get_uri(file)
        print('SEARCH ',i, file)
        
        if tmp != None:
            if len(genres) == 0:
                try:
                    artistk = tmp['album artist']
                except Exception:
                    artistk = tmp['artist']
                genres = emotion_helper.get_artist_genres(artistk)
                for gen in genres:
                    xlibstr += gen + ';'

            tmp['genres'] = xlibstr
            uri_totalfiles.append(tmp)
            

    uri_index = emotion_helper.int_index_to_uri_index(uri_totalfiles)

    print("Getting spotify data for found entries:", len(uri_index))
    totalfiles = emotion_helper.get_spotify_data(uri_index) 

    for daaggiornare, audiof in totalfiles.items():
        print('UPDATING ', daaggiornare)
        try:
            km = audiof
            process_audiofile(km)
            done+=1
        except Exception as e:
            print ('Error: '+ str(e))
    print('END. DONE: ', done)
    print('END. NOT DONE: ', totsize - done)
    return done

def process_audiofile(km):
    audiofile = eyed3.load(km['file_location'])
    newg = str(km['genres'])
    audiofile.tag.user_text_frames.set(newg,"SPTY_GENRE" )
    audiofile.tag.user_text_frames.set(str(km['tempo']),"SPTY_TEMPO" )
    audiofile.tag.user_text_frames.set(str(km['mode']),"SPTY_MODE" )
    audiofile.tag.user_text_frames.set(str(km['uri']),"SPTY_URI" )

    try:
        oldgenre = audiofile.tag.genre.name
    except Exception:
        oldgenre = None      
             
    if (oldgenre is None or len(oldgenre) == 0) and len(newg)>0:
        audiofile.tag.user_text_frames.set(newg,"SPTY_GENRE_REVIEW" )
    elif oldgenre in newg and len(newg)>len(oldgenre):
        audiofile.tag.user_text_frames.set(newg,"SPTY_GENRE_REVIEW" )
    elif newg in oldgenre:
        audiofile.tag.user_text_frames.set(oldgenre,"SPTY_GENRE_REVIEW" )
    else:#non trovato
        audiofile.tag.user_text_frames.set(oldgenre+';'+newg,"SPTY_GENRE_REVIEW" )
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
    start_letter = 't'
    end_letter = 'z'
    for root, dirs, files in os.walk("E:\\Musica", topdown=True):
        for i,name in enumerate(dirs):
            if name[0].lower() >= start_letter and name[0].lower() < end_letter  :
                print(str(i)+"/"+str(len(dirs)) +"PROCESS: ", root+ '\\' +name)  
                res += parse_Dir(root+ '\\' +name)
                print(str(i)+"/"+str(len(dirs))+"PROCESSED "+ root+ '\\' +name + ': ' + str(res)) 
            else:
                print('Skipping '+ name)



