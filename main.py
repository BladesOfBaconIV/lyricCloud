from wordcloud import WordCloud
from bs4 import BeautifulSoup
from urllib import request
from collections import Counter
from os import path, makedirs

URL_ROOT = 'http://www.sabaton.net'

if not path.exists('output'):
    makedirs('output')

html = request.urlopen(URL_ROOT + '/discography/')
soup = BeautifulSoup(html, 'html.parser')

album_links_html = soup.find('div', class_='elementor-element elementor-element-353ce1e8 elementor-column elementor-col-50 elementor-top-column').find_all('a')
album_links = [link['href'] for link in album_links_html]

def wordcloud_for_album(album_link):
    html = request.urlopen(URL_ROOT + album_link)
    soup = BeautifulSoup(html, 'html.parser')

    lyric_link_htmls = soup.find_all('a', text='Lyrics')
    links = [link['href'] for link in lyric_link_htmls]
    
    album_name = album_link.replace('/discography/', '').replace('/', '')
    print(album_name)
    if not path.exists('output/' + album_name):
        makedirs('output/' + album_name)
    output_folder = 'output/' + album_name + '/'

    song_lyrics = {}
    for link in links:
        song_name = link.replace('/discography/', '').replace('/', '')
        print(song_name)
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
        WordCloud().generate(lyrics).to_file(output_folder + song_name + '.jpg')

    WordCloud().generate(album_lyrics).to_file(output_folder + album_name + '.jpg')

for album in album_links:
    wordcloud_for_album(album)