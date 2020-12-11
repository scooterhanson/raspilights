import wiringpi2 as wiringpi, time, random
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(101, 0x20)   # set up the pins and i2c address  
wiringpi.mcp23017Setup(117, 0x21)
wiringpi.mcp23017Setup(133, 0x22)
print ('I2C Testing Section')
print ('.')
for x in range (101,149):
	wiringpi.pinMode(x, 1)         # sets GPA0 to output  



# Start Clean UP
for x in range (101, 149): # clean up
        wiringpi.digitalWrite(x,0)

# exit



