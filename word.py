#!/usr/bin/env python
# -*- coding:utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def wordcloud(f):
    '''
    plot the most frequently words
    '''
    print("\nIn the processing of calculate the times of each words appear...")

    wordc = WordCloud(
            background_color="white",  # change the color of background into white
            width=1500,              # set the width of pictures
            height=960,              # set the high of pictures
            margin=5
            ).generate(f)

    # draw picture
    fig = plt.figure()
    plt.imshow(wordc)
    # eliminate the axises
    plt.axis("off")
    plt.title("Most frequent words songs' names")
    # show pictures
    plt.show()
    # save pictures
    fig.savefig("wordcloud.jpg")
