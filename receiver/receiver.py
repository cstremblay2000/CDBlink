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

# debugging and logging constants
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

def parse_cli_args():
    """
    description:
        process commandline arguments, 
        check -h for help 
    """
    # init parses and add arguments
    parser = argparse.ArgumentParser( description="Process arguments" )
    parser.add_argument( '-e', '--encoding', \
                         choices=['morse', 'ascii'], \
                         help="encoding for recieved message, default ascii" )
    parser.add_argument( 'filepath' )
    parser.add_argument( '-c', '--crop', \
                         nargs=4, \
                         metavar='N', 
                         type=int, \
                         help="x y w h -> crop image bounded by (x+w,y+h)") 
    parser.add_argument( '-C', '--channel', 
                         choices=['r','g','b', 'none'],\
                         help="Specify which channel to pull out and use to" +\
                         " binarize image, default is green" )
    
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

    # process arguments and populate relevant flags
    parsed      = parser.parse_args() 
    ENCODING    = parsed.encoding
    FILEPATH    = parsed.filepath
    if( parsed.crop != None ):
        CROP    = True
        X       = parsed.crop[0]
        Y       = parsed.crop[1]
        DX      = parsed.crop[2]
        DY      = parsed.crop[3]
    if( parsed.channel != None ):
        CHANNEL = parsed.channel
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
    cap = cv.VideoCapture( FILEPATH )
    logging.debug( "Opening file '%s'" % FILEPATH )

    # get frame rate 
    fps = cap.get(cv.CAP_PROP_FPS)
    logging.debug( "framerate %d" % fps )
    
    # create debug windows
    if( logging.root.level <= logging.DEBUG ):
        cv.namedWindow( NAMED_WINDOW, cv.WINDOW_NORMAL )
        cv.namedWindow( NAMED_WINDOW1, cv.WINDOW_NORMAL )

    # start processing video frame by frame
    frame_total = 1
    light_is_on = False
    frames_on = 0
    frames_off = 0
    on_list = list()
    off_list = list()

    while( cap.isOpened() ):
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
        blur    = cv.GaussianBlur( frame, (5,5), 0 )
        
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
                break
    cap.release()

    # show results
    logging.debug( "on list" + str(on_list) )
    logging.debug( "off list" + str(off_list) )
    times = [e/fps for e in on_list]
    print( "durations light is on", times )

if( __name__ == "__main__" ):
    parse_cli_args()

    logging.basicConfig( level=LOGGING_LEVEL, format=FORMAT )
    main()
