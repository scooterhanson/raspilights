import Queue
import threading
#from multiprocessing import Process, Queue
import wiringpi2 as wiringpi
import time
import mido
import json
import subprocess
import pygame
import sys

def setupIO():
    wiringpi.wiringPiSetup()                    # initialise wiringpi
    wiringpi.mcp23017Setup(101, 0x20)   # set up the pins and i2c address
    wiringpi.mcp23017Setup(117, 0x21)
    wiringpi.mcp23017Setup(133, 0x22)
    for x in range (101,149):
            wiringpi.pinMode(x, 1)         # sets GPA0 to output

def allPinsOff():
    # Start Clean UP
    for x in range (101, 149): # clean up
        wiringpi.digitalWrite(x,1)


def setupMidiData():
    midimapping = {}
    mapFile = '/home/pi/dev/raspilights/midimap.json'
    with open(mapFile) as midi_data:
        data = json.load(midi_data)
        for row in data['relay-mapping']:
            midimapping[row['note']] = row['relay']
    return midimapping

def setupPlaylist():
    playlist = {}
    playlistFile = '/home/pi/dev/raspilights/playlist.json'
    with open(playlistFile) as playlist_data:
        data = json.load(playlist_data)
        for row in data['song-mapping']:
            song = {}
            song['midi'] = row['midi']
            song['ticks'] = row['ticks']
            song['offset'] = row['offset']
            song['vol'] = row['vol']
            playlist[row['audio']] = row
    return playlist

def setupAudio(vol):
    subprocess.call(["amixer","sset","PCM",vol])

def playAudio(audio, offset):
#    while q.empty():
#        # wait until the midi messages have been loaded into the queue
#        continue
    print 'audio offset: %s' % offset
    time.sleep(offset)
    print 'loading audio: %s' % audio
    pygame.mixer.init()
    song = pygame.mixer.Sound(audio)
    print "playing audio"
    song.play()
    pygame.time.wait(int(song.get_length() * 1000)) #do we need this?
    print "finished audio"

def playMidi(song,q):
    mid = mido.MidiFile(song['midi'])
    #mid.ticks_per_beat = song['ticks']#15550 #15360 orig
    #print 'ticks per beat: %s' % mid.ticks_per_beat
    print "playing midi"
    for msg in mid.play(meta_messages=True):
    #for msg in mid.play():
        #print str(msg)
        q.put("start")
        try:
            msg_items = str(msg).split();
            msg_note_val = msg_items[2]
            note_num = int(msg_note_val.split('=')[1])
            relay = midimapping[note_num]
        except:
            #print "Bad message"
            continue
        if(msg_items[0] == 'note_on'):
            #time.sleep(.01)
            wiringpi.digitalWrite(relay, 0)
        if(msg_items[0] == 'note_off'):
            #time.sleep(.01)
            wiringpi.digitalWrite(relay, 1)
    print "finished midi"

setupIO()
allPinsOff()
midimapping = setupMidiData()
playlist = setupPlaylist()

hour = time.strftime("%H")
maxHour = 23

while int(hour) < maxHour:
    for audio,song in playlist.items():
        try:
            setupAudio(song['vol'])
            #q = Queue()
            q = Queue.Queue()
            t1 = threading.Thread(target=playMidi, args = (song,q,))
            t1.start()

            t2 = threading.Thread(target = playAudio, args = (audio,song['offset'],))
            t2.start()


            t1.join()
            t2.join()

#            p1 = Process(target = playMidi, args = (song,q,))
#            p1.start()
#            p2 = Process(target = playAudio, args = (audio,song['offset'],))
#            p2.start()
#            print "a"
#            p1.join()
#            print "b"
#            p2.join()
#            print "c"
            hour = time.strftime("%H")
            allPinsOff()
        except KeyboardInterrupt:
            allPinsOff()
            t1.terminate()
            t2.terminate()
#            p1.terminate()
#            p2.terminate()
            sys.exit(1)
