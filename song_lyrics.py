from lyrics_extractor import Song_Lyrics
import settings
import re

extract_lyrics = Song_Lyrics(settings.GCS_API_KEY, settings.GCS_ENGINE_ID)

def song_lyrics(song_msg):
    result = re.finditer('"([^"]*)"', song_msg)
    len, itterator = getIterLenAndIter(result)
    if len <= 0:
        return 'please search as : lyrics for "your_song_name"\n              or \ncheck your internet Connection'
    else:
        for res in itterator:
            song_name = res.group()
            song_name = song_name.replace('"', '')

    title, lyrics = extract_lyrics.get_lyrics(song_name)
    return title, lyrics

def getIterLenAndIter(iterator):
    temp = list(iterator)
    return len(temp), iter(temp)

# content = song_lyrics('lyrics for "shape of you"')
# if type(content) == str:
    # print(content)
# if type(content) == tuple:
    # for data in content:
        # print(data)

