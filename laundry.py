import argparse

parser = argparse.ArgumentParser(
        description='Query LaundryView-enabled machines in Princeton.')
parser.add_argument('query', metavar='MACHINE',
        help='Name of hall (not case-sensitive)')
parser.add_argument('--verbose', dest='verbose', action='store_true',
        help='Print long-form output.')

args = parser.parse_args()

import urllib2
import re
import json

with open('rooms.json') as datafile:
    rooms = json.load(datafile)

room = ('', -1)
for k in rooms:
    q = args.query.lower()
    name = k.lower()
    if name.startswith(q):
        room = (k,rooms[k])
        break

if room[1] == -1:
    print 'error: cannot find room called: '+args.query
    exit()
if args.verbose:
    print 'loading room: '+room[0]

url = 'https://laundryview.com/dynamicRoomData.php?location='+str(room[1])
raw = urllib2.urlopen(url).read()

raw = raw[1:]
statuses = raw.split('&')[2:]
l = [a.strip().split('\n') for a in statuses]
flat = [item for sublist in l for item in sublist]

def parse(text):
    ind = text.find('=')
    if ind != -1:
        text= text[ind+1:]
    array = text.split(':')
    return array
q = map(parse, flat)
for i in q:
    print i
