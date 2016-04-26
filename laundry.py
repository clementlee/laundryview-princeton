import urllib2
import re

raw = urllib2.urlopen('https://laundryview.com/dynamicRoomData.php?location=3073421').read()

raw = raw[1:]
statuses = raw.split('&')[2:]
l = [a.strip().split('\n') for a in statuses]
flat = [item for sublist in l for item in sublist]

def parse(text):
    ind = text.find('=')
    if ind != -1:
        text= text[ind+1:]
    array = text.split(':')
    return text.split(':')
q = [parse(a) for a in flat]
for i in q:
    print i
