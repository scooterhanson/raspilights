# Compiled by Joseph Dix, no rights reserved.
# this is to test 32 relays connected to 2 mcp23017
# see this in action @ Raspberry Pi with 32 relays and 2 mcp23017 
# http://youtu.be/m83UdW67hVY
import wiringpi2 as wiringpi, time, random
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(101, 0x20)   # set up the pins and i2c address  
wiringpi.mcp23017Setup(117, 0x23)
print ('I2C Testing Section')
print ('.')
for x in range (101,133):
	wiringpi.pinMode(x, 1)         # sets GPA0 to output  
#Start all relays on/off in unison
print('Start All On and Off')
for loop in range (0, 15):
	for x in range (101, 133):
		wiringpi.digitalWrite(x,0)
	time.sleep(.1)
	for x in range (101, 133):
		wiringpi.digitalWrite(x,1)
	time.sleep(.1)
#Start 1 on/off at a time
print('Start 1 on/off at a time')
L = 3 # number of loops
S = (.02) # delay between loops
for run_a in range (0,L):
	for x in range (101,133):
		wiringpi.digitalWrite(x, 1)
		time.sleep(S)
		wiringpi.digitalWrite(x, 0)  
		time.sleep(S * 2)
		wiringpi.digitalWrite(x, 1)
		time.sleep(S)
# Randomizer
L = 401 # number of loops
S = .015 # delay between loops

# Begin Random relay
print('Start Randomizer')
for run in range (0, L):
        onoff = random.randint(0,1)
        rand = random.randint(101, 133)
        wiringpi.digitalWrite(rand,onoff)
        time.sleep(S)
for x in range (101, 133): #clean up
        wiringpi.digitalWrite(x,1)

# Sequencing
L = 20 # number of loops
print('Start Sequencing')
for run_s in range (0, L):
	for x in range (101, 133): # power on evens
		if x % 2 == 0:
			wiringpi.digitalWrite(x,0)
		else:	wiringpi.digitalWrite(x,1)
	time.sleep(.15)
	for y in range (101, 133): # power on odds
		if y % 2 != 0: 
			#print(y)
			wiringpi.digitalWrite(y,0)
		else:	wiringpi.digitalWrite(y,1)
	time.sleep(.15)
# Start Clean UP
for x in range (101, 133): # clean up
        wiringpi.digitalWrite(x,1)

# exit



