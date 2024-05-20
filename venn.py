import os
 
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io
import eyed3
import emotion_helper
ROOT_DIR = "E:\\Musica\\"
def parse_Dir(direct:str,total_songs:list) -> list:
    '''Parsa e processa una dir'''
    done=0
    #totsize = 0
    directory = direct

    totalfiles = emotion_helper.import_from_dir(directory)
    for it in totalfiles:
        try:
            audiofile = eyed3.load(it['file_location'])
            total_songs.append(audiofile)
        except Exception:
            pass

if __name__ == '__main__':
    total_songs:list[eyed3.AudioFile] = []
    genre_set = set()
     
    for root, dirs, files in os.walk(ROOT_DIR, topdown=True):
         
        for i,name in enumerate(dirs):
            #print(str(i)+"/"+str(len(dirs)) +" PROCESS: ", root+ '\\' +name)  
            parse_Dir(root+ '\\' +name,total_songs)
    
    tagged_totalfiles = []
    chart3d_df = pd.DataFrame(columns=['song','title', 'energy', 'valence', 'loudness', 'genre','album','artist'])
      
    for i,file in enumerate(total_songs):
        tit = file.tag.title
        album = file.tag.album
        artist = file.tag.artist
        album_artist = file.tag.album_artist
        try: 
            valence = float(file.tag.user_text_frames.get('SPTY_VALENCE').text)
            energy = float(file.tag.user_text_frames.get('SPTY_ENERGY').text)
            loud = float(file.tag.user_text_frames.get('SPTY_LOUDNESS').text)
            genre = file.tag.genre.name.split('\x00',10)[0]
        except Exception as e:
            print ('emotion_helper.get_tags Error: '+ str(e))
            valence = 0
            energy = 0
            loud = 0
            genre = 'NA'
            
             
        chart3d_df.loc[i] = [file.path,tit ,energy ,valence, loud,genre,album,artist]             
   
        

    #fill DONE, draw emotion 3D chart
    df2=chart3d_df[chart3d_df["genre"] != 'NA'] 
    chart3d_df.to_csv('out.csv', index=False, encoding="utf-8")
    fig = px.scatter_3d(df2, x='energy', y='valence', z='loudness',
                        color='genre', hover_name='song')
    fig.show()

    #Genre chart
    fig2 = px.histogram(chart3d_df, x='genre', height=800,barmode='group', title="Generi musicali", color="artist", text_auto=True)
    fig2.show()
