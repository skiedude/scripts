import RPi.GPIO as GPIO
import time as t
from datetime import datetime, time

#17 red
#22 blue
#23 green
allLights = [17,22,23]

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(allLights, GPIO.OUT, initial=GPIO.LOW)

def tearDown():
    GPIO.cleanup()

def turnOnLight(pinNumber):
    GPIO.output(pinNumber, GPIO.HIGH)
    for l in allLights:
        if l != pinNumber:
            turnOffLight(l)

def turnOffLight(pinNumber):
    GPIO.output(pinNumber, GPIO.LOW)

def getHourMin():
    return datetime.now().hour, datetime.now().minute

def timeTillSleep():
    timeHour,timeMin = getHourMin()
    timeHourDiff = (19 - timeHour) - 1
    if timeHourDiff > 0:
        totalHourSec = (timeHourDiff * 60) * 60
        print(f"Sleeping {timeHourDiff} hours")
        t.sleep(totalHourSec)

def checkTime():
    timeHour,timeMin = getHourMin()
    if timeHour >= 7 and timeHour < 8:
        if not GPIO.input(23):
            print(f"{datetime.now().time()} Turning on Green, we are free!")
            turnOnLight(23)
        else:
            print(f"{datetime.now().time()} already Green")

    elif timeHour >= 19 or timeHour < 6:
        if not GPIO.input(17):
            print(f"{datetime.now().time()} Turning on Red, go to bed!")
            turnOnLight(17)
        else:
            print(f"{datetime.now().time()} already Red")
    elif timeHour == 6: 
        if not GPIO.input(22):
            print(f"{datetime.now().time()} Turning on Blue")
            turnOnLight(22)
        else:
            print(f"{datetime.now().time()} already Blue")
    else:
        print(f"{datetime.now().time()} No light time")
        turnOffLight(23)
        timeTillSleep()

try:
    GPIO.setwarnings(False)
    setup()
    while True:
        checkTime()
        t.sleep(300)
except KeyboardInterrupt:
    tearDown()
    print('Exiting')
except Exception as e:
    tearDown()
    print(f'Failed with {e}')
