#!/usr/bin/env python
from __future__ import print_function, division
import sys
import argparse
import mido
from mido import MidiFile, Message, tempo2bpm


def play_file(filename, print_messages):
    midi_file = MidiFile(filename) 

    print('Playing {}.'.format(midi_file.filename))
    length = midi_file.length
    print('Song length: {} minutes, {} seconds.'.format(
            int(length / 60),
            int(length % 60)))
    print('Tracks:')
    for i, track in enumerate(midi_file.tracks):
        print('  {:2d}: {!r}'.format(i, track.name.strip()))

    for message in midi_file.play(meta_messages=True):
        if print_messages:
            sys.stdout.write(repr(message) + '\n')
            sys.stdout.flush()

        if isinstance(message, Message):
            sys.stdout.write("")
            sys.stdout.flush()
            #output.send(message)
        elif message.type == 'set_tempo':
            print('Tempo changed to {:.1f} BPM.'.format(
                tempo2bpm(message.tempo)))

    print()


def main():
    try:
        play_file("jingle.mid",True)
    except KeyboardInterrupt:
        pass


main()
