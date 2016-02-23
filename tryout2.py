# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 08:32:12 2016

@author: Adam Gao
"""

# Word Cloud generation

## 1 single word, single color, single font, multiple sizes


import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sklearn.feature_extraction.text import CountVectorizer
from pandas import Series,DataFrame
import pandas as pd

# initalize
word = 'Word Cloud'
WIDTH = 500
HEIGHT = 500
img = Image.new("RGB",(WIDTH,HEIGHT),color = (0,0,0))
draw = ImageDraw.Draw(img)
FONT1 = 'C:\Windows\Fonts\FELIXTI.TTF'
draw.text((5,0), "Word Cloud-v0 by Adam Gao", fill=(200,200,200),font =ImageFont.truetype('C:\Windows\Fonts\ARESSENCE.ttf', size=15))


def check_occupied(pos,sz):
    if(pos[0]+sz[0]>=WIDTH or pos[1]+sz[1]>=HEIGHT): return True
    for i in range(sz[0]):
        for j in range(sz[1]):
            if(img.getpixel((pos[0]+i,pos[1]+j)) != (0,0,0)): return True
    return False

def add_word(img,word,below):
    sz = int(50*(1-below)) + 5 # min size = 10  
    pos = (np.random.random_integers(WIDTH),np.random.random_integers(HEIGHT))
    TRY = 0
    while check_occupied(pos,draw.textsize(word,ImageFont.truetype(FONT1, size=sz))):
        TRY += 1
        sz = max(sz - int(TRY/10),10)
        pos = (np.random.random_integers(WIDTH),np.random.random_integers(HEIGHT))
    print TRY
    
    if(np.random.randint(2)==1): FONT = ImageFont.TransposedFont(ImageFont.truetype(FONT1,size=sz),orientation = Image.ROTATE_90)
    else: FONT = ImageFont.truetype(FONT1,size=sz)
    draw.text(pos, word,font=FONT, fill=(np.random.random_integers(155)+100,np.random.random_integers(255),np.random.random_integers(155)+100))

def main1():
    N = 100
    for i in range(N):
        add_word(img,word,i/N)
    img.save('D:\\SelfLearning\\WordCloud\\WordCloud.png')




## 2 different words

f = open('D:\\SelfLearning\\WordCloud\\shakespeare_154verses.txt')
lines = f.readlines()
text = ''.join(lines)

cv = CountVectorizer(max_features=200)
counts = cv.fit_transform([text]).toarray().ravel()
words = np.array(cv.get_feature_names())

stoplist = ['is','are','in','be','it','an','as','also','if','does','do','a','for','and','but','from','any','by','all','have','get','into','only','of','or',
            'should','this','either','than','not','off','on','before','the','none','out','against','am']
data = DataFrame({'words':words,'counts':counts})
for stopword in stoplist:
    data = data[data['words'] != stopword]

counts = counts / float(counts.max())
counts = counts ** 2 # curve a little bit


def main2():
    N = len(data)
    for i in range(N):
        if(words[i] not in stoplist):
            add_word(img,words[i],counts[i])
    #img.save('WordCloud.png','png')
    img.show()

main2()
