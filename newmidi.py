#!/usr/bin/env python

import midicludge as midiparser
#import midiparser as midiparser


midi = midiparser.File('/home/pi/dev/raspilights/jingle.mid')
	
#print "\nMIDI file:\n	%s" % os.path.basename(args.infile.name)
print "MIDI format:\n	%d" % midi.format
print "Number of tracks:\n	%d" % midi.num_tracks
print "Timing division:\n	%d" % midi.division

noteEventList=[]
all_channels=set()

for track in midi.tracks:
    channels=set()
    for event in track.events:
        if event.type == midiparser.meta.SetTempo:
            tempo=event.detail.tempo
            print "Tempo change: " + str(event.detail.tempo)
        if (event.type == midiparser.voice.NoteOn): # filter undesired instruments

            if event.channel not in channels:
                channels.add(event.channel)

            # NB: looks like some use "note on (vel 0)" as equivalent to note off, so check for vel=0 here and treat it as a note-off.
            if event.detail.velocity > 0:
                noteEventList.append([event.absolute, 1, event.detail.note_no, event.detail.velocity])
                print("Note on  (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
            else:
                noteEventList.append([event.absolute, 0, event.detail.note_no, event.detail.velocity])
                print("Note off (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
        if (event.type == midiparser.voice.NoteOff):

            if event.channel not in channels:
                channels.add(event.channel)

            noteEventList.append([event.absolute, 0, event.detail.note_no, event.detail.velocity])
            print("Note off (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
noteEventList.sort()

for note in noteEventList:
#    print note
# note[timestamp, note off/note on, note_no, velocity]
#    if last_time < note[0]:
    duration=0
    last_time = 0
#        # Get the duration in seconds from the MIDI values in divisions, at the given tempo
    duration = ( ( ( note[0] - last_time ) + 0.0 ) / ( midi.division + 0.0 ) * ( tempo / 1000000.0 ) )
    
    print "duration: %s"%duration
    print "note: %s"%note[2]
    print "on/off: %s"%note[1]
