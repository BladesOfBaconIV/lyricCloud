from wordcloud import WordCloud
from search_parameters import artist_search_params, album_search_params
import requests
import json

API_ROOT = 'https://api.musixmatch.com/ws/1.1/'

artist_search_response = requests.get(API_ROOT + 'artist.search', params=artist_search_params).json()
ARTIST_ID = artist_search_response['message']['body']['artist_list'][0]['artist']['artist_id']

album_search_params['artist_id'] = ARTIST_ID
album_response = requests.get(API_ROOT + 'artist.albums.get', params=album_search_params).json()

album_json_list = album_response['message']['body']['album_list']
album_dict = {}
for album_json in album_json_list:
    album = album_json['album']
    album_dict[album['album_name']] = album['album_id']
