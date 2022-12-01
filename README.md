# CDBlink
Modulates reading and writing data to a USB CD drive to make the onboard LED blink 

## Sender

### Overview
This Python script will modulate the activity of an optical disk drive to transmit data. It requires a message to transmit and an encoding scheme to use. This can be provided via arguments or durring runtime. When providing the message to transmit via arguments you may provide either a string or a file containing the message to read. You can also provide a block length to the script to control the length of read operations used durring transmission, this optional. Once the message and codec are set the message will be encoded. Then the script will transmit the message by using Linux's dd utility to access the optical drive with device file `/dev/sr0`. It will first spin up the optical drive via a large read operation and then transmit the message via the appropriate function for the codec in use. When the message has been transmitted the script will print "Complete" and end.

### How this should be used
This is a proof of concept script to show that the behaviour of an optical drive's access light can be modulated to encode and trasmit data. It should be used for research and further development of this covert channel.

### Dependancies
- [Python3](https://www.python.org/downloads/)
- An optical disk drive

### How to run
- To run without arguments use `python3 transmitter.py`
- To run via arguments with a message use `python3 transmitter.py -c [codec choice] -m [message]`
- To use an input file use `python3 transmitter.py -c [codec choice] -f [path to file]`
- To set block size via argument use `python3 transmitter.py -b [block length]`

### Usage Message
```
CD-Blink Covert Channel Transmitter
usage: transmitter.py [-h] [-c CODEC] [-m MSG | -f FILE] [-b BLKL]

CD-Blink Encoding and Transmission

options:
  -h, --help            show this help message and exit
  -c CODEC, --codec CODEC
                        Encoding Scheme: 1 = Morse(Alphanumeric Only) 2 = On-
                        Off-Keying 3 = Binary Frequency Shift Keying
  -m MSG, --msg MSG     Message to transmit
  -f FILE, --file FILE  File to read message from
  -b BLKL, --blkl BLKL  Length in KB of 1 unit for reading
```

## Receiver

### Overview
The python script will initially read in a video specified by the user, or by specifying a number of the device to be used. The
program will then start to process each frame and it through an
image processing pipeline. First it will crop the image (if
specified by the user), then it will split the image into each color channel.
By default, the green channel is used. Using connected component analysis, the
script counts the number of black and white blobs. If any white blobs exist in
the frame, then that frame will be interperted as having a light present. If a
blob doesn't exist, then it will be interperted as not having a light present.
The script then counts the number of frames where the light is on, and uses the
frame rate of the video to then determine the duration of time the light was on
for.

### How this should be used
The idea to use this program is to crop out a small rectangle around the light
being observed. This means that the user should know the coordinates of the
top left corner, width, and height of the bounding rectangle to isolate the
light. This can easily be found by adding the `-d` flag. This will bring up the 
native OpenCV image windows where the user can view the coordinates of the pixels. 

### Dependencies
- [Python3](https://www.python.org/downloads/)
- OpenCV2, `pip3 install opencv-python`
- numpy, `pip3 install numpy`

### How to run
- To run the program with a pre-recorded video use `python3 receiver.py [filename]`
- To run the program with a connected camera use `python3 receiver.py 0`, or replace 0 with a number until you get the stream you want.

### Usage message
```
usage: receiver.py [-h] [-e {morse,bfsk,ook}] [-c N N N N] [-C {r,g,b,none}] [-d] filepath

decode a message from flashing lights

positional arguments:
  filepath              path to filepath, or number of device to stream from

options:
  -h, --help            show this help message and exit
  -e {morse,bfsk,ook}, --encoding {morse,bfsk,ook}
                        morse, binary frequency shift keying, on-off keying. Default morse
  -c N N N N, --crop N N N N
                        x y W H -> crop image to a rectangle of WxH, with top left corner at (x,y)
  -C {r,g,b,none}, --channel {r,g,b,none}
                        Specify which channel to pull out and use tobinarize image, default is green
  -d, --debug           debugging mode
```
