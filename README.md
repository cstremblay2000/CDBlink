# CDBlink
Modulates reading and writing data to a USB CD drive to make the onboard LED blink 

## Sender

## Receiver

### Overview
The python script will initially read in a video specified by the user. The
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
native OpenCV image windows where the user can view the coordinates of the pixes. 

### Dependencies
- [Python3](https://www.python.org/downloads/)
- OpenCV2, `pip3 install opencv-python`
- numpy, `pip3 install numpy`

### How to run
- To run the program use `python3 receiver.py [filename]`

### Usage message
```
usage: receiver.py [-h] [-e {morse,ascii}] [-c N N N N] [-C {r,g,b,none}] [-d]
                   filepath

decode a message from flashing lights

positional arguments:
  filepath

options:
  -h, --help            show this help message and exit
  -e {morse,ascii}, --encoding {morse,ascii}
                        encoding for recieved message, default morse
  -c N N N N, --crop N N N N
                        x y dx dy -> crop image bounded by (x+dx,y+dy)
  -C {r,g,b,none}, --channel {r,g,b,none}
                        Specify which channel to pull out and use tobinarize
                        image, default is green
  -d, --debug           debugging mode
```
