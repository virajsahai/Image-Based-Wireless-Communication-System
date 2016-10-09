This project implements a base concept for communicating data using patterns and pictures, wherein, your monitor acts as a transmitter and the camera acts as a receiver.

The motivation behind the project was to entriely cut off the keylogging attacks for stealing sensitive information of internet users.

As of now the system only transmits one character at a time and can be improved to transmit many characters simultaneouly and use the FPS capacity of the camera to transfer as much data as possible. Also, since this is just a protoype the system uses bluetooth to transmit the encryption keys. The proposed system was for online banking systems and the detailed design uses GSM networks to transmit keys. The system can also be improved to incorporate private encrypting/decrypting algorithms. Feel free to ping me at virajsahai32@hotmail.com or vsahai@usc.edu in case you want to work with me to make it a real worls usable system.

SOME IMPORTANT POINTS-----

1. The message to be transmitted should be placed in the TM.txt file.
2. Before using the code make sure to update the Bluetooth Address of the receiver device in the Transmitter.py file.
3. Make sure to update your camera index number in the Receiver.py file.
4. The pattern2.txt file shows how each character is mapped where S="Square" T="Triangle" C="Circle" X="Cross" A="Arrow"
   H="Arrow Head"
5. The ASCII codes and the Patterns have been matched in one-to-one sequential pattern.
6. Before using the system don't forget to install the respective libraries.