#!/usr/bin/python

import time
from threading import Thread
import mido
import datetime as dt
import json
import wiringpi2 as wiringpi, time, random


wiringpi.wiringPiSetup()                    # initialise wiringpi
wiringpi.mcp23017Setup(101, 0x20)   # set up the pins and i2c address
wiringpi.mcp23017Setup(117, 0x21)
wiringpi.mcp23017Setup(133, 0x22)
for x in range (101,149):
    wiringpi.pinMode(x, 1)         # sets GPA0 to output


midimapping = {}
playlist = {}

with open('midimap.json') as midi_data:
    data = json.load(midi_data)
    for row in data['relay-mapping']:
        midimapping[row['note']] = row['relay']

with open('playlist.json') as playlist_data:
    index = 0
    data = json.load(playlist_data)
    for row in data['playlist']:
        playlist[index]['audio'] = row['audio']
        playlist[index]['midi'] = row['midi']
        index += 1


print midimapping


cur_time = dt.datetime.now() 

#>>> import datetime as dt
#>>> n1=dt.datetime.now()
#>>> n2=dt.datetime.now()
#>>> (n2-n1).microseconds
#678521
#>>> (n2.microsecond-n1.microsecond)/1e6
#0.678521



mid = mido.MidiFile('rockin.mid')
for msg in mid.play():
    print(msg)
#    new_time = dt.datetime.now() 
    msg_items = str(msg).split();
    msg_note_val = msg_items[2]
    msg_note_len = msg_items[4]
    note_num = int(msg_note_val.split('=')[1])
    note_len = float(msg_note_len.split('=')[1])
    relay = midimapping[note_num]
    if(msg_items[0] == 'note_on'):
        print ('NOTE: %s  --  RELAY ON: %s'%(note_num,relay))
        wiringpi.digitalWrite(relay, 0)
    if(msg_items[0] == 'note_off'):
        print ('NOTE: %s  --  RELAY OFF: %s'%(note_num, relay))
        wiringpi.digitalWrite(relay, 1)

#        new_time = dt.datetime.now()
#        time_diff = new_time - cur_time
#        print (time_diff)
#        print('NUM: %s, LEN: %s'%(note_num, note_len))
#    cur_time = new_time    

