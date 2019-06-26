import requests
from zipfile import ZipFile
import os.path
from xml.dom import minidom


def _decompress(file_path, directory):
    with ZipFile(file_path, 'r') as zipHandler:
        # Extract all the contents of zip file in current directory
        zipHandler.extractall(directory)


def _save_database(request, file_path):
    with open(file_path, 'wb') as database_file:
        print(request.headers)
        print(request.content)
        for chunk in request.iter_content(chunk_size=128):
            database_file.write(chunk)


def __find_localized_description(localized_descriptions, locale):
    for localized_description in localized_descriptions:
        if localized_description.getAttribute('lang') == locale:
            return localized_description
    return None


def read_titles_from_database(locale, directory):
    titles = {}
    database = minidom.parse(os.path.join(directory, 'wiitdb.xml'))
    games = database.getElementsByTagName('game')
    for game in games:
        localized_descriptions = game.getElementsByTagName('locale')
        description = __find_localized_description(localized_descriptions, locale)
        if description is None:
            description = __find_localized_description(localized_descriptions, 'EN')
        titles[game.getElementsByTagName('id')[0].childNodes[0].data.strip()] = description.getElementsByTagName('title')[0].childNodes[0].data.strip()
    return titles


def load(locale, directory):
    params = {'LANG': locale, 'WIIWARE': 1, 'GAMECUBE': 1}
    with requests.get('https://www.gametdb.com/wiitdb.zip',
                      params=params,
                      headers={"Accept": "text/html", "Accept-Encoding": "gzip, deflate", "User-Agent": "Mozilla/5.0"},
                      stream=True) as response:
        print("loading database from GAMETDB website : %s" % response.url)
        print(response.status_code)
        if response.status_code == 200:
            if response.headers.get('Content-Disposition'):
                _save_database(response, 'wiitdb.zip')
                _decompress('wiitdb.zip', directory)