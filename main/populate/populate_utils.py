import urllib.parse
import urllib.request

BASE_URL = 'https://www.wikidex.net/wiki'


def open_url(url):
    cod_url = urllib.parse.quote(url, safe=':/?=')
    try:
        req = urllib.request.urlopen(cod_url)
        return req.read()
    except:
        print(f'----------Error---------- URL: {cod_url}')
        return None
