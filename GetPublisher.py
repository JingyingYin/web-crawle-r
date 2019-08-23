#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib

from NameTransfer import trans2


def get_publisher(singer):
    '''
    get the publishers which published news of  the typical singer
    :param singer:
    :return list of publishers:
    '''
    publishers = []
    param = {'andtext': trans2(singer), 'format': 'json'}
    # change the string which will be used in links into the needed format
    newslink = 'https://chroniclingamerica.loc.gov/search/pages/results/?'+urllib.parse.urlencode(param)
    req = urllib.request.Request(newslink)
    html = urllib.request.urlopen(req, timeout=500).read()  # read all the content of that link
    infos = json.loads(html)
    if len(infos) > 0:
        for info in infos['items']:
            # reach main part where the songs are
            publishers.append(info['publisher'])
    return publishers


def test():
    temp = get_publisher('ColdPlay')
    assert len(temp) is not 0

    print("Test pass!")


if __name__ == '__main__':
    test()
