# -*- coding: utf - 8 - *-
"""
Created on Mon Jan 18 20:37:13 2016

@author: Adam Gao
"""

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sklearn.feature_extraction.text import CountVectorizer
from pandas import Series, DataFrame
import pandas as pd
import random as rd

# Initializing canvas

default_stoplist = ['is', 'are', 'in', 'be', 'it', 'an', 'as', 'also', 'if', 'does', 'do', 'a', 'for', 'and', 'but', 'from', 'any', 'by', 'all', 'have', 'has', 'get', 'into', 'only', 'of', 'or', 'should', 'this', 'these', 'that', 'either', 'than', 'not', 'off', 'on', 'before', 'the', 'none', 'out', 'against', 'am', 'to', 'at']


class mask(object):
    def __init__(self, directory=None, shape=None):
        self.pixels = []
        pass
        # set the size equal to the size of WordCloud Canvas


class WordCloud(object):
    def __init__(self, width, height, background=(0, 0, 0), stoplist=default_stoplist):
        self.width = width
        self.height = height
        self.background = background
        self.img = Image.new('RGB', (self.width, self.height), color=self.background)
        self.stoplist = stoplist

    def get_words(self, directory, max_words=200):
        # open file
        f = open(directory)
        lines = f.readlines()
        text = ''.join(lines)

        # get words
        cv = CountVectorizer(max_features=max_words)
        counts = cv.fit_transform([text]).toarray().ravel()
        words = np.array(cv.get_feature_names())
        data = DataFrame({'words': words, 'counts': counts})

        for stopword in self.stoplist:
            data = data[data['words'] != stopword]
        data['counts'] = (data['counts'] / float(data['counts'].max())) ** 0.85  # curve a little bit
        return data

    def draw(self, directory, fontdir, max_size=50, min_size=5, max_words=200, margin=2):
        def find_empty_area(x_range, y_range):
            empty_area = []
            for i in x_range:
                for j in y_range:
                    if self.img.getpixel == self.background:
                        empty_area.append((i, j))
            return empty_area
        # initializing empty area
        # empty_area = find_empty_area(range(self.width), range(self.height))

        def check_occupied(pos, occupy):
            if(pos[0] + occupy[0] + margin >= self.width or pos[1] + occupy[1] + margin >= self.height):
                return True
            for i in range(occupy[0] + margin):
                for j in range(occupy[1] + margin):
                    if(self.img.getpixel((pos[0] + i, pos[1] + j)) != self.background):
                        return True
            return False

        def add_word(word, count):
            draw = ImageDraw.Draw(self.img)
            size = int((max_size - min_size) * count) + min_size
            # pos = (rd.sample(empty_area[0], 1),  rd.sample(empty_area[1], 1))
            pos = (np.random.random_integers(self.width), np.random.random_integers(self.height))
            if(np.random.randint(3) == 0):
                font = ImageFont.TransposedFont(ImageFont.truetype(fontdir, size), orientation=Image.ROTATE_90)
            else:
                font = ImageFont.truetype(fontdir, size)
            occupy = draw.textsize(word, font)

            TRY = 0
            while check_occupied(pos, occupy):
                pos = (np.random.random_integers(self.width), np.random.random_integers(self.height))
                TRY += 1
            print 'word:', word, 'size = %d' % size, 'TRY:%d' % TRY

            draw.text((pos[0] + 1 + (size >= 50), pos[1] + 1 + (size >= 50)), word, font=font, fill=(170, 170, 170))  # shade

            red = (255, -int(255 * count) + 175, -int(255 * count) + 175)
            blue = (-int(255 * count) + 175, -int(255 * count) + 175, 255)
            green = (-int(255 * count) + 175, 255, -int(255 * count) + 175)
            yellow = (255, 255, -int(255 * count) + 175)
            orange = (255, (red[1] + yellow[1]) / 2, -int(255 * count) + 175)

            draw.text(pos, word, font=font, fill=(rd.sample([red, blue, orange], 1)[0]))
            # draw.text(pos, word, font = font, fill = (np.random.random_integers(255), np.random.random_integers(255), np.random.random_integers(255) ))

        data = self.get_words(directory, max_words).sort_values(by='counts', ascending=False)
        for i in data.index:
            if(data['words'][i] not in self.stoplist):
                add_word(data['words'][i], data['counts'][i])
        # img.save('WordCloud_v1.png', 'png')
        self.img.show()


def main():
    w = WordCloud(800, 600, background=(244, 244, 244))
    w.draw('Data\\The Declaration of Independence.txt', 'Fonts\\FTLTLT.TTF', max_size=120, min_size=15, max_words=120, margin=2)

main()


# More features to be added:
# automatically switch to upper()
# more beautiful color pallete
# MASK
