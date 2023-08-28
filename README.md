SpotifyTagger

Starting from [Lucy-In-The-Sky-With-Emotion](https://github.com/brentvollebregt/Lucy-In-The-Sky-With-Emotion) code, I wrote a simple spotify mood tagger.

It writes new ID3 TAG on SPTY_* of TXX user Tags. An audio player like MusicBee will be then configured to highlight the new features, configured as "ratings"
Some hand work is necessary to configure visualization and filtering with these new SPTY_ tags

![Added TAGS](https://i.imgur.com/J6HGkae.png)

![An example rule configured inside mp3 player](https://i.imgur.com/6oQoFNv.png)



# Instructions

update settings.json
insert target dir in main
python simple_index.py
