import webbrowser
import re

def getIterLenAndIter(iterator):
    temp = list(iterator)
    return len(temp), iter(temp)

def search(query_msg):
    result = re.finditer('"([^"]*)"', query_msg)
    len, itterator = getIterLenAndIter(result)
    if len <= 0:
        return 'please search as : search for "Your_query"\n              or \ncheck your internet Connection'
    else:
        for res in itterator:
            query = res.group()
            query = query.replace('"', '')

    tab_url = "http://google.com/?#q="
    webbrowser.open_new_tab(tab_url + query)


# search('search for "elephant"')
