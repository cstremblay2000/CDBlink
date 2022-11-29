# CDBlink
Modulates reading and writing data to a USB CD drive to make the onboard LED blink 

## Sender

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
