# raspilights

This is a crazy project for controlling a musical holiday lights show.  I built a toolbox-based controller for 48 independent outlets, driven by relays, controlled by a Raspberry Pi and a custom i2c breakout board ased on the [MCP23017](http://raspi.tv/2013/using-the-mcp23017-port-expander-with-wiringpi2-to-give-you-16-new-gpio-ports-part-3) chip.

![](https://github.com/scooterhanson/raspilights/blob/main/xmaslightboard1.jpg)

The breakout board is this piece here:

![](https://github.com/scooterhanson/raspilights/blob/main/xmaslighti2cboard.jpeg)

I use midi files to sequence the lights, with linkages defined between note values and relay addresses in *midimap.json*.  Creating the midi files is a whole other discussion.  I first loaded the wav file into a digital audio workstation, corrected the timing through the song, and then recorded the notes that corresponded to each individual light string into a midi track.  It takes a while to set up each midi file, but the *note_on* and *note_off* messages make it very convenient to turn on and off the relays. [mido](https://mido.readthedocs.io/en/latest/) makes it incredibly easy to parse through a midi file and read each message, which then get parsed into a queue.

The file *raspilights.py* was my original attempt that uses a subprocess call to *play* for wav file playback.  This led to wildly unpredictable differences in when the music started vs. when the light sequence started.  It works ok, but I wanted more control.

*pg_raspilights.py* uses [pygame](https://www.pygame.org/news) to playback the wav file and it's timed to start as soon as the midi messages start getting parsed into the thread queue.

So, the only major dependencies are mido and pygame.

