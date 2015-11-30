#!/usr/bin/python

#-------------------------------------------------------------------------------
# Name:        Attendance
# Purpose:     Read NFC tag, then send to SjtekControl
#
# Author:      Jakub 'Yim' Dvorak,
#              Wouter 'Whhoesj' Habets
#
# Created:     26.10.2013
# Copyright:   (c) Jakub Dvorak 2013
# Licence:
#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Jakub Dvorak wrote this file. As long as you retain this notice you
#   can do whatever you want with this stuff. If we meet some day, and you think
#   this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

# Python 2
from urllib2 import Request, urlopen, URLError, HTTPError

# Python 3
# import urllib.request

continue_reading = True


def end_read(signal,frame):
    global continue_reading
    print ""
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    print ""

def millis():
    return int(round(time.time() * 1000))

def main():

    # Capture SIGINT for cleanup when the script is aborted

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    previousCard = ""
    lastReadTime = 0
    readDelay = 4000


    # Welcome message
    print "Welcome to the MFRC522 data read example"
    print "Press Ctrl-C to stop."


    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            cardId = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])



            print "Time " + str(millis()) + " - " + str(lastReadTime) + " - " + str(readDelay)

            if (millis() - lastReadTime) > readDelay:
                lastReadTime = millis()
                print "Time elapsed"
                url = "http://sjtek.nl/api/nfc/read?cardid=" + cardId
                print "Sending... " + url

                # Python 2
                req = Request(url)
                try:
                    response = urlopen(req)
                except HTTPError as e:
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
                except URLError as e:
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                else:
                    pass
                    # everything is fine

                # Python 3
                # urllib.request.urlopen(url).read()

                print "Send"
                pass
            else:
                print "Time not elapsed"

            print ""

if __name__ == '__main__':
    main()
