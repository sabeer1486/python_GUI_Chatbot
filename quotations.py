import requests
import settings

def get_quotations():
    quote = requests.get("http://quotes.rest/qod.json?category=inspire")
    data = quote.json()
    quote = data["contents"]["quotes"][0]["quote"]
    author = data["contents"]["quotes"][0]["author"]
    response = "*Quote of the day.*\n\n" + quote + "\n - _*" + author + "*_"
    return response

# print(get_quotations())