import requests

def fetchAndSaveToFile(url, path):
    r = requests.get(url)
    with open(path, 'wb') as f:  # use 'wb' for binary mode
        f.write(r.content)

url = 'https://www.flipkart.com/search?q=iq+neo+9+pro&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=iq+neo+9+pro%7CMobiles&requestId=6a4822fe-ca2a-4717-bc61-c6da27782254'
fetchAndSaveToFile(url, 'scrapping.html')
