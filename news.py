try:
    import bitly_api
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please read this article to install Bitly_api: https://www.geeksforgeeks.org/python-how-to-shorten-long-urls-using-bitly-api/")
import requests
import settings

def get_news():
    """
        Fetches latest news from News API.
        Collects the top 5 news from google news.
        Shortens news links using Bitly APIs.
        Returns Aggregated news.
    """
    b = bitly_api.Connection(access_token = settings.BITLY_ACCESS_TOKEN) 
    url = "https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=" + settings.NEWS_API_KEY

    news = requests.get(url)
    data = news.json()
    title = []
    description = []
    short_link = []
    for i in range(5):
        title.append(data["articles"][i]["title"])
        description.append(data["articles"][i]["description"])
        link = data["articles"][i]["url"]
        flink = b.shorten(uri=link)
        short_link.append(flink["url"])

    return title, description, short_link

# title, description, short_link = get_news()
# for i in range(5):
#     print(title[i], description[i], short_link[i])
    