# CDBlink
Modulates reading and writing data to a USB CD drive to make it blink to encode data

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

### Dependencies
- [Python3](https://www.python.org/downloads/)
- OpenCV2, `pip3 install opencv-python`
- numpy, `pip3 install numpy`

### How to run
- To run the program use `python3 receiver.py [filename]`
- To see and example checkout `receiver/test_mp4.sh` 
