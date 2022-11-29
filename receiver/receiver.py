"""
file:       receiver.py
language:   Python3
author:     Chris Tremblay <cst1465@rit.edu>
date:       10/18/2022, National Chocolate Cupcake Day!
description:
    Receives a message from a blinking light using openCV2
"""

import cv2 as cv
import numpy as np
import sys
import logging
import argparse
import math
import decoders

# debugging and logging constants
<<<<<<< HEAD:reciever/receiver.py
NW_ORIG         = "original"
NW_CROP         = "cropped"
NW_BLUR         = "blurred"
NW_GRAY         = "grayscale"
NW_BIN          = "binarize"
LOGGING_LEVEL   = logging.INFO

# populated after command line args are parsed
FILEPATH    = ""
CROP        = False
X           = 0
Y           = 0
DX          = 0
DY          = 0
ENCODING    = "morse"
CHANNEL     = 'g'
DECODER     = None
=======
NAMED_WINDOW    = "w1"
NAMED_WINDOW1   = "w2"
FORMAT          = "[%(levelname)s %(funcName)-10s] %(message)s"
LOGGING_LEVEL   = logging.DEBUG

# populated after command line args are parsed
FILEPATH    = ""        # path to video
CROP        = False     # crop image at all
X           = 0         # top left corner, for cropping
Y           = 0         # top right cornerm for cropping
DX          = 0         # how much rectangle extends right
DY          = 0         # how much rectangle extends down
ENCODING    = "ascii"   # how blinks are interpurted
DOT         = 100       # ms
DASH        = 300       # ms
SPACE       = 500       # ms
CHANNEL     = 'g'       # which color channel to pull out
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py

def parse_cli_args():
    """
    description:
        process commandline arguments, 
        check -h for help 
    """
    # init parses and add arguments
    parser = argparse.ArgumentParser( description="decode a message from " +
            "flashing lights" )
    parser.add_argument( '-e', '--encoding', \
<<<<<<< HEAD:reciever/receiver.py
                         choices=['morse', 'bfsk','ook'],\
                         help="morse, binary frequency shift keying, " +
                               " on-off keying. Default morse",
                         default='morse' )
=======
                         choices=['morse', 'ascii'], \
                         help="encoding for recieved message, default ascii" )
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py
    parser.add_argument( 'filepath' )
    parser.add_argument( '-c', '--crop', \
                         nargs=4, \
                         metavar='N', 
                         type=int, \
                         help="x y W H -> crop image to a rectangle of" +\
                         " WxH, with top left corner at (x,y)" ) 
    parser.add_argument( '-C', '--channel', 
                         choices=['r','g','b', 'none'],\
                         help="Specify which channel to pull out and use to" +\
<<<<<<< HEAD:reciever/receiver.py
                         "binarize image, default is green" )
    parser.add_argument( '-d', '--debug', help='debugging mode', \
                         action='store_true' )
=======
                         " binarize image, default is green" )
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py
    
    # init variables as global
    global FILEPATH
    global CROP
    global X 
    global Y 
    global DX
    global DY
    global ENCODING
    global DOT
    global DASH
    global SPACE
    global CHANNEL
    global DECODER
    global LOGGING_LEVEL

    # process arguments and populate relevant flags
    parsed      = parser.parse_args() 
    ENCODING    = parsed.encoding
    if( ENCODING == 'morse' ):
        DECODER = decoders.decode_morse
    elif( ENCODING == 'bfsk' ):
        DECODER = decoders.bfsk_decode
    elif( ENCODING == 'ook' ):
        DECODER = decoders.ook_decode
    FILEPATH    = parsed.filepath
    if( parsed.crop != None ):
        CROP    = True
        X       = parsed.crop[0]
        Y       = parsed.crop[1]
        DX      = parsed.crop[2]
        DY      = parsed.crop[3]
    if( parsed.channel != None ):
        CHANNEL = parsed.channel
    if( parsed.debug ):
        LOGGING_LEVEL = logging.DEBUG
    logging.basicConfig( level=LOGGING_LEVEL )
    return

def light_on( binarized, connectivity:int=4 ) -> bool:
    """
    description:
        Using connected components analysis, checks if there is a light
        detected in the given frame
    parameters:
        binarized       -> the frame in black and white 
        connectivitiy   -> the connectivity passed to cv2.connectedComponents 
    returns: 
        True more than 1 blob is detected, false otherwise
    """
    # connnected component analysis
    ret, labels = cv.connectedComponents( binarized, connectivity )

    # pull out analysis
    min_val, max_val, _, _ = cv.minMaxLoc( labels )
    logging.debug( "min %d max %d" % (min_val, max_val ) ) 
    return max_val >= 1

def main():
    """
    description:
        The driver function
    """
    # open video 
    if( FILEPATH.isnumeric() ):
        cap = cv.VideoCapture( int(FILEPATH) )
        logging.info( "detected device, press Ctrl-C to exit when done" )
    else:
        cap = cv.VideoCapture( FILEPATH )
    logging.debug( "Opening file '%s'" % FILEPATH )

    # get frame rate 
    fps = cap.get( cv.CAP_PROP_FPS )
    logging.debug( "framerate %d" % fps )
    
    # create debug windows
    if( logging.root.level <= logging.DEBUG ):
        cv.namedWindow( NW_ORIG, cv.WINDOW_NORMAL )
        if( CROP ):
            cv.namedWindow( NW_CROP, cv.WINDOW_NORMAL )
        cv.namedWindow( NW_BLUR, cv.WINDOW_NORMAL )
        cv.namedWindow( NW_GRAY, cv.WINDOW_NORMAL )
        cv.namedWindow( NW_BIN, cv.WINDOW_NORMAL )

    # start processing video frame by frame
    frame_total             = 1
    light_is_on             = False
    frames_on               = 0
    frames_off              = 0
    on_list                 = list()
    off_list                = list()

    while( cap.isOpened() ):
<<<<<<< HEAD:reciever/receiver.py
        try:
            # get frame and check that it exists
            ret, frame = cap.read()
            orig = frame.copy()
            if( not ret ):
=======
        # get frame and check that it exists
        ret, frame = cap.read()
        if( not ret ):
            break
        if( logging.root.level <= logging.DEBUG ):
            cv.imshow( NAMED_WINDOW1, frame )

        # crop image if specified by cli
        if( CROP ):
            frame = frame[Y:Y+DY,X:X+DX]

        # keep track of frames for debugging
        logging.debug( "frame: %d" % frame_total )
        frame_total += 1

        # blur image and split into 3 color channels
        blur = cv.GaussianBlur( frame, (5,5), 0 )
        
        # pull out channel if specified
        channel = None
        if( CHANNEL[0] != 'n' ):
            b,g,r   = cv.split( frame )
            if( CHANNEL == 'r' ):
                channel = r
            elif( CHANNEL == 'g' ):
                channel = g
            elif( CHANNEL == 'b' ):
                channel = b
        else: # grayscale channel to threshold it to binary later
            channel = cv.cvtColor( frame, cv.COLOR_BGR2GRAY )
         
        # binarize image, turn black and white
        # use green channel since lights used for testing are green
        ret, binarized = cv.threshold( channel, 127, 255, cv.THRESH_BINARY )

        # check if light on 
        if( light_on( binarized ) ):
            if( not light_is_on ):
                logging.debug( "light turned on" )
                off_list.append( frames_off )
                frames_off = 0
            frames_on += 1
            light_is_on = True
        else:
            if( light_is_on ):
                logging.debug( "light turned off" )
                light_is_on = False
                on_list.append( frames_on )
                frames_on = 0
            frames_off += 1

        # show it
        if( logging.root.level <= logging.DEBUG ):
            cv.imshow( NAMED_WINDOW, binarized )
            k = cv.waitKey( 0 )
            if( k == ord( 'q' ) ):
                cv.destroyAllWindows()
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py
                break

            # crop image if specified by cli
            if( CROP ):
                frame = frame[Y:Y+DY,X:X+DX]
                cv.rectangle( orig, (X,Y), (X+DX,Y+DY), (0,0,255), 5 )

            # show orignal with rectangle around cropped area
            if( logging.root.level <= logging.DEBUG ):
                cv.imshow( NW_ORIG, orig )
                cv.imshow( NW_CROP, frame )

            # keep track of frames for debugging
            logging.debug( "frame: %d" % frame_total )

            # blur image and split into 3 color channels
            # a 5x5 gaussian filter
            # | 1  4  7  4  1 |
            # | 4 16 26 16  4 |    1
            # | 7 26 41 26  7 | X ---
            # | 4 16 26 16  4 |   273
            # | 1  4  7  4  1 |
            #
            # a 3x3 mean filter
            # | 1 1 1 |   1
            # | 1 1 1 | X -
            # | 1 1 1 |   9
            blur = cv.GaussianBlur( frame, (5,5), 0 )
            if( logging.root.level <= logging.DEBUG ):
                cv.imshow( NW_BLUR, frame )

            # pull out channel if specified
            channel = None
            if( CHANNEL[0] != 'n' ):
                b,g,r   = cv.split( frame )
                if( CHANNEL == 'r' ):
                    channel = r
                elif( CHANNEL == 'g' ):
                    channel = g
                elif( CHANNEL == 'b' ):
                    channel = b
            else: # grayscale channel to threshold it to binary later
                channel = cv.cvtColor( frame, cv.COLOR_BGR2GRAY )

            if( logging.root.level <= logging.DEBUG ):
                cv.imshow( NW_GRAY, channel )

            # binarize image, turn black and white
            # use green channel since lights used for testing are green
            ret, binarized = cv.threshold( channel, 127, 255, cv.THRESH_BINARY )
            if( logging.root.level <= logging.DEBUG ):
                cv.imshow( NW_BIN, binarized )

            # check if light on 
            if( light_on( binarized ) ):
                if( not light_is_on ):
                    logging.debug( "light turned on" )
                    off_list.append( frames_off )
                    frames_off = 0

                frames_on += 1
                light_is_on = True
            else:
                if( light_is_on ):
                    logging.debug( "light turned off" )
                    light_is_on = False
                    on_list.append( frames_on )
                    frames_on = 0
                frames_off += 1

            # exit
            if( cv.waitKey(1) & 0xFF == ord('q') ):
                break
            frame_total += 1
        except KeyboardInterrupt:
            break

    cap.release()
<<<<<<< HEAD:reciever/receiver.py
    if( logging.root.level == logging.DEBUG ):
        cv.destroyAllWindows()

    logging.debug( "on list" + str(on_list) )
    logging.debug( "off list" + str(off_list) )
    times_on  = [e/fps for e in on_list]
    times_off = [e/fps for e in off_list ]
=======

    # show results
    logging.debug( "on list" + str(on_list) )
    logging.debug( "off list" + str(off_list) )
    times = [e/fps for e in on_list]
    print( "durations light is on", times )
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py

    print( times_on )
    print( times_off )
    print( "recieved msg:", DECODER( times_on, times_off ) )
    print( "time to xmit:", sum( times_on ) + sum( times_off[1:len(times_on)]))
    
if( __name__ == "__main__" ):
    parse_cli_args()
<<<<<<< HEAD:reciever/receiver.py
=======
    logging.basicConfig( level=LOGGING_LEVEL, format=FORMAT )
>>>>>>> ce2effcf9531807ebe67be446ad1e5a6f1734bb3:receiver/receiver.py
    main()
