#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    Transform the singers' names into the format which api needs
'''


def trans1(singer):
    '''
    transform into format of the link which can find songs
    :param singer:
    :return transfromed name:
    '''
    singer = singer.split()
    insert = '-'.join(singer)
    return insert


def trans2(singer):
    '''
    transform into format of the link which can find publishers
    :param singer:
    :return transfromed name:
    '''
    singer = singer.split()
    insert = singer[0]
    return insert
