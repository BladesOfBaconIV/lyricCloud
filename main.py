from wordcloud import WordCloud
from bs4 import BeautifulSoup
from urllib import request
from collections import Counter

URL_ROOT = 'http://www.sabaton.net'
album_link = '/discography/heroes-album/'

html = request.urlopen(URL_ROOT + album_link)
soup = BeautifulSoup(html, 'html.parser')

link_htmls = soup.find_all('a', text='Lyrics')

links = [link['href'] for link in link_htmls]

song_lyrics = {}

for link in links:
    song_name = link.replace('/discography/', '').replace('/', '')
    html = request.urlopen(URL_ROOT + link)
    soup = BeautifulSoup(html, 'html.parser')
    lyrics_box = soup.find_all('div', class_='elementor-text-editor elementor-clearfix')[1]
    for br in lyrics_box.find_all('br'):
        br.replace_with(' ')
    text_blocks = lyrics_box.find_all('p')[1:] # skip the first one as it is publisher info
    lyrics = ' '.join([verse.text for verse in text_blocks])
    song_lyrics[song_name] = lyrics

album_lyrics = ' '.join([track_lyrics for track_lyrics in song_lyrics.values()])

for song, lyrics in song_lyrics.items():
    WordCloud().generate(lyrics).to_file('output/' + song + '.jpg')

WordCloud().generate(album_lyrics).to_file('output/heroes.jpg')

if 're' in album_lyrics:
    print('why?')