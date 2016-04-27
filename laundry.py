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
with open('roomdata.json') as datafile:
    roomdata = json.load(datafile)

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
statuses = raw.split('&')#[2:]
l = [a.strip().split('\n') for a in statuses]
flat = [item for sublist in l for item in sublist]

def parse(text):
    ind = text.find('=')
    if ind != -1:
        text= text[ind+1:]
    array = text.split(':')
    return array
q = map(parse, flat)
q = filter(lambda x: len(x) == 10, q)

#for i in q:
#    print i

w = 0
wa = 0
d = 0
da = 0
#print roomdata
for i in q:
    if i[3] in roomdata[str(room[1])] and i[2] != '1':
        if roomdata[str(room[1])][i[3]] == True:
            w += 1
            if i[0] == '1':
                wa += 1
        else:
            d += 1
            if i[0] == '1':
                da += 1

print "%d of %d washers available" % (wa, w)
print "%d of %d dryers available" % (da, d)
