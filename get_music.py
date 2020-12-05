import pafy
import re
import requests
from bs4 import BeautifulSoup
try:
    import bitly_api
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please read this article to install Bitly_api: https://www.geeksforgeeks.org/python-how-to-shorten-long-urls-using-bitly-api/")
import settings


def music(song_msg):
    """
        Takes song_name as an argument.
        Formats the song name and passes it to Youtube Data API.
        It then extracts teh video id and title from the first Youtube result.
        The video is converted into an Audio with Medium Bitrate settings.
        Audio and Video is formatted and shortened using Bitly API.
        Returns title, audio link and video link as a tuple.
    """
    # gets quoted string 
    result = re.finditer('"([^"]*)"', song_msg)
    len, itterator = getIterLenAndIter(result)
    if len <= 0:
        return 'please search as : linten to "your_song_name"\n              or \ncheck your internet Connection'
    else:
        for res in itterator:
            song_name = res.group()
            song_name = song_name.replace('"', '')

    b = bitly_api.Connection(access_token = settings.BITLY_ACCESS_TOKEN) 
    song_name = song_name + " song"

    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + song_name + \
        "&key=" + settings.YTDATA_API_KEY + "&maxResults=1&type=video"

    page = requests.get(url)
    data = page.json()
    sear = data["items"][0]["id"]["videoId"]
    title = data["items"][0]["snippet"]["title"]

    myaud = pafy.new(sear)
    genlink = myaud.audiostreams[2].url
    vlink = "https://www.youtube.com/watch?v=" + sear

    flink = b.shorten(uri=genlink)
    flink = flink["url"]
    vlink = b.shorten(uri=vlink)
    vlink = vlink["url"]

    return (title, flink, vlink)

def getIterLenAndIter(iterator):
    temp = list(iterator)
    return len(temp), iter(temp)


# print(music('listen to "despacito"'))
