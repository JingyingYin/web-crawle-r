#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import word


def analysis():

    '''
    draw conclusion from the data set
    '''

    sql_name = 'singers_info.sqlite'
    conn = sqlite3.connect(sql_name)
    cur = conn.cursor()
    print('calculating the conclusion...\n')

    # select data from database, figure out the number of songs each singer published
    print('reading table 1...')
    cur.execute('''SELECT Singers.singer_name, count(song.song_name)
        FROM song, Singers
        WHERE Singers.s_ID=song.singer_ID 
        GROUP BY song.singer_ID''')
    content1 = cur.fetchall()
    content1 = pd.DataFrame(content1)  # transform into DataFrame
    content1.sort_values(0, inplace=True)  # sort data by the name of singers
    content1.reset_index(drop=True, inplace=True)
    print('done with table 1')

    # select data from database, figure out the number of publishers which reported the singer
    print('reading table 2...')
    cur.execute('''SELECT singers.singer_name, count(publisher.publisher_name) 
        FROM publisher, Singers
        WHERE Singers.s_ID=publisher.singer_ID 
        AND publisher.publisher_name NOT NULL
        GROUP BY publisher.singer_ID''')
    content2 = cur.fetchall()
    content2 = pd.DataFrame(content2)  # transform into DataFrame
    content2.sort_values(0, inplace=True)  # sort data by the name of singers
    content2.reset_index(drop=True, inplace=True)
    print('done with table 2')

    content = pd.concat([content1, content2.iloc[:, 1]], axis=1)  # connect two DataFrame
    content.columns = ['singer', 'count_song', 'count_publisher']  # reset the column name
    content.sort_values('count_song', inplace=True)  # sort data by the numbers of songs
    content.reset_index(drop=True, inplace=True)

    # get the songs that published by Taylor Swift
    cur.execute('''SELECT Singers.singer_name,count(song.song_name)
        FROM song, Singers
        WHERE Singers.s_ID=song.singer_ID
        AND Singers.singer_name LIKE '%taylor%'
        GROUP BY song.singer_ID''')
    taylor = cur.fetchone()
    print('\nthe singer: {} the number of published songs: {}'.format(taylor[0], taylor[1]))

    # get the singer name and songs number who published the most songs
    cur.execute('''SELECT singer_name, count(song.song_name) as num
        FROM song, Singers
        WHERE Singers.s_ID=song.singer_ID 
        GROUP BY song.singer_ID
        ORDER BY num DESC
        LIMIT 1''')
    band = cur.fetchone()
    print('\nthe singer: {} published most songs: {}'.format(band[0], band[1]))

    # prepare data for plot the relationship between song numbers and publishers
    content_t = content[content['count_song'] > 1]
    table = content_t.describe()
    print(table)

    #  select all the songs' names from database
    cur.execute('''SELECT song_name
            FROM song''')
    song = cur.fetchall()
    song = str(song)  # transform from list to string, prepare for analyze the frequency

    word.wordcloud(song)  # plot the most frequently words

    #  plot the relationship between song numbers and publishers
    fig = plt.figure()
    plt.plot(content_t.index, content_t.iloc[:, 2], label='number of publishers')  # number of publishers
    plt.plot(content_t.index, content_t.iloc[:, 1]/100, label='number of songs/100')  # number of songs
    plt.legend()  # show label
    plt.title('comparison of number of songs with publishers')  # picture title
    plt.show()
    plt.draw()
    fig.savefig("conclusion.jpg")  # save picture locally
    fig.savefig("conclusion.jpg")  # save picture locally

