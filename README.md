SpotifyTagger

Progetto rotto dal 2025 a causa di cambio policy API https://developer.spotify.com/documentation/web-api/reference/get-audio-analysis
andate a fanculo

Starting from [Lucy-In-The-Sky-With-Emotion](https://github.com/brentvollebregt/Lucy-In-The-Sky-With-Emotion) code, I wrote a simple spotify mood tagger.

It writes new ID3 TAG on SPTY_* of TXX user Tags. An audio player like MusicBee will be then configured to highlight the new features, configured as "ratings"
Some hand work is necessary to configure visualization and filtering with these new SPTY_ tags

![Added TAGS](https://i.imgur.com/J6HGkae.png)

![An example rule configured inside mp3 player](https://i.imgur.com/6oQoFNv.png)



# Instructions
- pip install requirements
- update settings.json using your own spotify API keys
- insert target dir in main inside simple_index.py
- run simple_index.py
