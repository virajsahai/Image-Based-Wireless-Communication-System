import cv2
import numpy as np
from bluetooth import *
from time import sleep
camera_port=1
ramp_frames=15
images=[]
camera=cv2.VideoCapture(camera_port)
##Synching
server_sock=BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port=server_sock.getsockname()[1]
uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee"
advertise_service(server_sock,"SampleServer",
                  service_id=uuid,
                  service_classes=[uuid,SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE]
                  )
print "Waiting for transmitter."

client_sock,client_info=server_sock.accept()
print "Ready to receive"

while True:
    data=client_sock.recv(1024)
    if data=='Ready':
        break
key_alpha=client_sock.recv(1024)
key_num=client_sock.recv(1024)
length=client_sock.recv(1024)
key_alpha=int(key_alpha)
key_num=int(key_num)
length=int(length)
i=length
##Image Capturing/Pre-Processing
images=[]
def get_image():
    retval, im=camera.read()
    return im
while True:
    sleep(2)
    if (i-2)==0:
        sleep(.5)
    for j in range(ramp_frames):
        temp = get_image()
    camera_capture=get_image()
    images.append(camera_capture)
    i-=1
    if i==0:
        break
for i in range(0,length):
    cv2.imwrite(str(i)+'.jpg',images[i])
##Decoding
symbols=["SquareNewG223.jpg","TriangleG223.jpg","CircleNewG223.jpg","XrossG223.jpg","ArrowG223.jpg","HeadG223.jpg"]
fin_seq=''
enc_message=''
pattern_file=open('pattern2.txt','r')
pattern=pattern_file.read().split('\n')
ascii_file=open('ascii.txt','r')
ascii=ascii_file.read().split('\n')
methods='cv2.TM_CCOEFF_NORMED'
for l in range(0,length):
    image=cv2.imread(str(l)+'.jpg',0)
    t=True
    seq=dict()
    fin_seq=''
    while t:
        for symbol in symbols:
            template=cv2.imread(symbol,0)
            G=template.copy()
            gpA=[G]
            for k in xrange(5):
                G=cv2.pyrDown(G)
                gpA.append(G)
            n=0
            for x in gpA:
                w,h=x.shape[::-1]
                method=eval(methods)
                res=cv2.matchTemplate(image,x,method)
                min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
                if max_val>0.50:
                    seq[max_loc[0]]=symbol[0]
                    t=False
                    break
                n=n+1
    for z in sorted(seq):
        fin_seq+=seq[z]
    for w in range(0,104):
        if pattern[w]==fin_seq:
            enc_message+=chr(int(ascii[w]))
            break
##Decrypting
translated=''
for symbol in enc_message:
    if symbol.isalpha():
        num=ord(symbol)
        num-=key_alpha
        if symbol.isupper():
            if num<ord('A'):
                num+=26
        elif symbol.islower():
            if num<ord('a'):
                num+=26
        translated+=chr(num)
    elif symbol.isdigit():
        num=ord(symbol)
        num-=key_num
        if num<ord('0'):
            num+=10
        translated+=chr(num)
    else:
        translated+=symbol
print "Received Message:",translated
client_sock.close()
server_sock.close()
print "Transmission Complete"
