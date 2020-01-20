import urllib.parse
import urllib.request

BASE_URL = 'https://www.wikidex.net'
WIKI_URL = f'{BASE_URL}/wiki'


def open_url(url):
    cod_url = urllib.parse.quote(url, safe=':/?=%')
    try:
        req = urllib.request.urlopen(cod_url)
        return req.read()
    except Exception as e:
        print(e)
        print(f'----------Error---------- URL: {cod_url}')
        return None
