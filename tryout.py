# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 06:08:01 2016

@author: Adam Gao
"""

# Word Cloud
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


f = open('Data\\wordcloud_text1.txt')
lines = f.readlines()
text = ''.join(lines)

cv = CountVectorizer()
counts = cv.fit_transform([text]).toarray().ravel()
words = np.array(cv.get_feature_names())

counts = counts / float(counts.max())


# a small test of PIL
img = Image.new("RGB",(500,500))
draw = ImageDraw.Draw(img)
font1 = ImageFont.truetype('C:\Windows\Fonts\COOPBL.TTF', 20)
draw.setfont(font1)
draw.text((60, 60), "First Wordle", fill="green")
font2 = ImageFont.truetype('C:\Windows\Fonts\ARBERKLEY.ttf', 25)
draw.setfont(font2)
draw.text((60, 70), "First Wordle", fill="yellow")
font3 = ImageFont.truetype('C:\Windows\Fonts\BROADW.TTF', 30)
draw.setfont(font3)
draw.text((60, 130), "First Wordle", fill="red")
font4 = ImageFont.truetype('C:\Windows\Fonts\ENGR.TTF', 30)
draw.setfont(font4)
draw.text((60, 165), "First Wordle", fill="purple")

draw.textsize('B')
img.save('Images\\img.png')

integral_image = np.cumsum(np.cumsum(img, axis=0), axis=1)

now = np.zeros(shape=(500,500),dtype=object)
now[4]

for i in range(500):
    for j in range(500):
        now[i,j] = img.getpixel((i,j))
        
a = img.getpixel((82,78))

pos = (60,62)
sz = (20,20)
def check_occupied(pos,sz):
    for i in range(sz[0]):
        for j in range(sz[1]):
            if(img.getpixel((pos[0]+i,pos[1]+j)) != (0,0,0)): return True
    return False
        

# test of wordcloud_text1.txt
