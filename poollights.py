from multiprocessing import Process, Queue
import wiringpi2 as wiringpi
import time
import mido
import json
import subprocess

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
    print 'audio offset: %s' % offset
    time.sleep(offset)
    start = time.time()
    print 'playing audio: %s' % audio
    subprocess.call(["play",audio])
    end = time.time()
    elapsed = end - start
    print("audio playtime: %s" % elapsed)

def playMidi(song,q):
    mid = mido.MidiFile(song['midi'])
    #mid.ticks_per_beat = song['ticks']#15550 #15360 orig
    #mid.ticks_per_beat = 15360 #orig
    print 'ticks per beat: %s' % mid.ticks_per_beat
    start = time.time()
    print 'playing midi %s' % song['midi']
    for msg in mid.play():
        q.put(msg)
    end = time.time()
    elapsed = end - start
    print("midi playtime: %s" % elapsed)
    q.put("break")

def workQueue(q):
    while 1:
        msg = q.get()
        if str(msg) == "break":
            break
        msg_items = str(msg).split();
        msg_note_val = msg_items[2]
        note_num = int(msg_note_val.split('=')[1])
        relay = midimapping[note_num]
        if(msg_items[0] == 'note_on'):
            wiringpi.digitalWrite(relay, 0)
        if(msg_items[0] == 'note_off'):
            wiringpi.digitalWrite(relay, 1)


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
            q = Queue()
            p1 = Process(target = playMidi, args = (song,q,))
            p1.start()
            p2 = Process(target = playAudio, args = (audio,song['offset']))
            p2.start()
            p3 = Process(target = workQueue, args = (q,))
            p3.start()
            p1.join()
            p2.join()
            p3.join()
            hour = time.strftime("%H")
            allPinsOff()
        except KeyboardInterrupt:
            allPinsOff()
            p1.terminate()
            p2.terminate()
            p3.terminate()
            sys.exit(1)
