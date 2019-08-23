#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sqlite3
import sys
import time
from GetPublisher import get_publisher
from GetSinger import get_singer
from GetSongs import get_songs
from conclusion import analysis
from progressbar import *


def main():
    if len(sys.argv) <= 1:
        print('Please enter an argument to specify the source mode!')
        return
    else:
        source = sys.argv[1]
        if source not in ['-source=remote', '-source=local']:
            print('please enter either "-source=remote" or "-source=local"')
            return
        temp = source.split('=')
        source = temp[1]
    print(' *  ----------------------------------------------------------------------------  * ')
    print(' |           PLEASE DO NOT CLOSE THE WEBSITE THAT WILL POP OUT SOON !!            | ')
    print(' |                  PLEASE MUST KEEP CHROMEDRIVER ON THIS FOLD!!                  | ')
    print(' *  ----------------------------------------------------------------------------  * ')

    try:
        '''
        try, in case of the database initialization failed
        '''
        sql_name = 'singers_info.sqlite'
        conn = sqlite3.connect(sql_name)
        cur = conn.cursor()

        '''
        Have to use remote type first to save the data locally, then be able to use local type to read data locally
        '''
        if source == 'remote':

            ''' 
            Build the DATABASE for saving information.
            '''

            cur.execute(''' DROP TABLE IF EXISTS Singers''')
            cur.execute(''' DROP TABLE IF EXISTS publisher''')
            cur.execute(''' DROP TABLE IF EXISTS song''')
            cur.execute('''CREATE TABLE Singers 
                        ( singer_name TEXT,
                          s_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE              
                    )''')

            cur.execute('''CREATE TABLE publisher 
                            ( publisher_name TEXT,
                              singer_ID INTEGER              
                        )''')
            cur.execute('''CREATE TABLE song 
                            ( song_name TEXT,
                              singer_ID INTEGER              
                        )''')
            print('get the list of singers, please wait ....')
            singers = get_singer()  # get the data of singer names
            print('successfully get the list of singers !!!')
            print('get the list of songs and publishers, please wait ....')
            i = 0

            progress = ProgressBar()

            for singer_ in progress(singers):
                time.sleep(0.03)
                '''
                saving singer names into database
                on table Singers, save the name of singers and their ID
                '''
                cur.execute('INSERT INTO Singers(singer_name) VALUES(?)', (singer_,))

                '''
                Get the singer's ID
                '''
                cur.execute('''SELECT s_ID
                        FROM Singers
                        WHERE singer_name = ?''', (singer_,))
                content = cur.fetchone()
                s_id = content[0]

                # print(i)
                i += 1
                try:  # in case of time out error
                    publishers = get_publisher(singer_)
                    if len(publishers) < 1:  # in case of there is no record for the publishers
                        cur.execute('INSERT INTO publisher(singer_ID) VALUES(?)', (s_id,))
                    else:
                        '''
                        saving the publisher into database
                        on table publisher, save the name of publishers and related singer's ID
                        '''
                        for publisher in publishers:
                            cur.execute('INSERT INTO publisher(publisher_name,singer_ID) VALUES(?,?)', (publisher, s_id,))

                    songs = get_songs(singer_)  # get the data of singer songs
                    if len(songs) < 1:  # in case of there is no record for the songs
                        cur.execute('INSERT INTO song(singer_ID) VALUES(?)', (s_id,))
                    else:
                        '''
                        saving the publisher into database
                        on table songs, save the name of songs and related singer's ID
                        '''
                        for song in songs:
                            cur.execute('INSERT INTO song(song_name,singer_ID) VALUES(?,?)', (song, s_id,))
                    conn.commit()
                except:
                    continue
                finally:
                    conn.commit()
            '''
                Output the description and sample output of data source 1
            '''
            print("*** Output data source 1 ***")
            print("> This data set contains the name, information and pictures of the singers.")
            print("> URL:\n\thttps://www.biography.com/people/groups/singer")
            print("> Sample output:")
            content = cur.execute('''SELECT *
                                        FROM Singers
                                        LIMIT 5''')
            for out in content:
                print(out)

            '''
                Output the description and sample output of data source 2
            '''
            print("*** Output data source 2 ***")
            print("> This data set contains all the information of all the news.")
            print("> URL:\n\thttps://chroniclingamerica.loc.gov/search/pages/results/?andtext=Kanye&format=json")
            print("> Sample output:")
            content = cur.execute('''SELECT *
                                FROM publisher
                                LIMIT 5''')
            for out in content:
                print(out)

            '''
                Output the description and sample output of data source 3
            '''
            print("*** Output data source 3 ***")
            print('''> This data set contains 
            all the songs that a specific band or a specific singer had published before.''')
            print("> URL:\n\thttps://www.oldies.com/artist-songs/Kanye-West.html")
            print("> Sample output:")
            content = cur.execute('''SELECT *
                                        FROM song
                                        LIMIT 5''')
            for out in content:
                print(out)

            print("\n\n ** let's draw some conclusions **\n")
            # analysis()

        else:
            '''
            Check weather the data have been already saved locally,
            '''
            cur.execute('''SELECT count(*) FROM Singers''')
            count = cur.fetchone()
            if count[0] == 0:
                print('Please use remote type to save data locally first !')
                return

            else:
                '''
                   Output the description and sample output of data source 1
               '''
                print("\n**Sample Results of Source 1**")
                print("> This data set contains the name, information and pictures of the singers.")
                print("> URL:\n\thttps://www.biography.com/people/groups/singer")
                print("> Sample output:")
                cont = cur.execute('''SELECT *
                            FROM Singers
                            LIMIT 5''')
                for i in cont:
                    print(i)

                '''
                    Output the description and sample output of data source 2
                '''
                print('\n**Sample Results of Source 2**')
                print("> This data set contains all the information of all the news.")
                print("> URL:\n\thttps://chroniclingamerica.loc.gov/search/pages/results/?andtext=Kanye&format=json")
                print("> Sample output:")
                cont = cur.execute('''SELECT *
                                    FROM publisher
                                    LIMIT 5''')
                for i in cont:
                    print(i)

                '''
                    Output the description and sample output of data source 3
                '''
                print('\n**Sample Results of Source 3**')
                print('''> This data set contains 
                all the songs that a specific band or a specific singer had published before.''')
                print("> URL:\n\thttps://www.oldies.com/artist-songs/Kanye-West.html")
                print("> Sample output:")
                cont = cur.execute('''SELECT *
                                    FROM song
                                    LIMIT 5''')
                for i in cont:
                    print(i)
        print("\n\n ** let's draw some conclusions **\n")
        analysis()
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == '__main__':
    main()
