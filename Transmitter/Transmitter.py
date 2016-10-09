import cv2
import numpy as np
from bluetooth import *
import sys
import random
from time import sleep
##For Synching
if sys.version<'3':
    input = raw_input
addr='68:5D:43:50:BF:21' #Bluetooth Address of Receiver Device
print("Searching for SampleServer")

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("Couldn't find the SampleServer service :(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Connecting")

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("Connected.")
message_file=open('TM.txt','r')
message=message_file.read()
message=str(message)

##Encrypting
key_alpha=random.randint(1,25) #Key for encrypting alphabets
key_num=random.randint(1,9)    #Key for encrypting digits
sock.send("Ready")
sleep(.25)
sock.send(str(key_alpha))
sleep(.25)
sock.send(str(key_num))
sleep(.25)
sock.send(str(len(message)))
translated=''
for symbol in message:
    if symbol.isalpha():
        num=ord(symbol)
        num+=key_alpha
        if symbol.isupper():
            if num>ord('Z'):
                num-=26
        elif symbol.islower():
            if num>ord('z'):
                num-=26
        translated+=chr(num)
    elif symbol.isdigit():
        num=ord(symbol)
        num+=key_num
        if num>ord('9'):
            num-=10
        translated+=chr(num)
    else:
        translated+=symbol
##Transmitting
pattern_file=open('pattern2.txt','r')
pattern=pattern_file.read().split('\n')
ascii_file=open('ascii.txt','r')
ascii=ascii_file.read().split('\n')
square=cv2.imread("SquareNew.jpg")
triangle=cv2.imread("Triangle.jpg")
circle=cv2.imread("CircleNew.jpg")
cross=cv2.imread("Cross.jpg")
arrow=cv2.imread("Arrow.jpg")
arrow_head=cv2.imread("Arrow Head.jpg")
background=cv2.imread("Background.jpg")
for x in translated:
    for y in range(0,104):
        control=0
        if x==chr(int(ascii[y])):
            control=1
            temp=pattern[y]
            if temp[0]=='S':
                output=square
            if temp[0]=='T':
                output=triangle
            if temp[0]=='C':
                output=circle
            if temp[0]=='X':
                output=cross
            if temp[0]=='A':
                output=arrow
            if temp[0]=='H':
                output=arrow_head
            for z in range(1,6):
                if temp[z]=='S':
                    output=np.hstack((output,square))
                if temp[z]=='T':
                    output=np.hstack((output,triangle))
                if temp[z]=='C':
                    output=np.hstack((output,circle))
                if temp[z]=='X':
                    output=np.hstack((output,cross))
                if temp[z]=='A':
                    output=np.hstack((output,arrow))
                if temp[z]=='H':
                    output=np.hstack((output,arrow_head))
            sleep(.5)
            cv2.namedWindow('Transmitting...')
            y_offset=275
            x_offset=125
            background[y_offset:y_offset+output.shape[0], x_offset:x_offset+output.shape[1]]=output 
            cv2.imshow('Transmitting...',background)
            cv2.resizeWindow('Transmitting...', 1366,768)
            cv2.waitKey(2250)
        if control==1:
            break
cv2.destroyWindow('Transmitting...')
sock.send("End")
print "Transmission Complete."
sock.close()
            
