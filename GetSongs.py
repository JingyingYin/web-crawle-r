#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from NameTransfer import trans1


def get_songs(singer):
    '''
    get the songs sung by the typical singer
    :param singer:
    :return list of songs:
    '''
    url = 'https://www.oldies.com/artist-songs/'+trans1(singer)+'.html'
    resp = requests.get(url)
    html = resp.content
    soup = BeautifulSoup(html, "lxml")
    contents = soup.select('span[class*="PLT"]')  # reach main table where the songs are
    songs = []
    for content in contents:
        # get songs' names in loop
        song = content.text.strip()  # remove the whitespace
        songs.append(song)  # save  songs' names into list
    return songs  # return that list


def test():
    temp = get_songs('Coldplay')
    assert len(temp) != 0

    print("Test pass!")


if __name__ == '__main__':
    test()
