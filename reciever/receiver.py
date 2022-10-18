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
LOGGING_LEVEL   = logging.DEBUG

# populated after command line args are parsed
FILEPATH    = ""
CROP        = False
X           = 0
Y           = 0
DX          = 0
DY          = 0
ENCODING    = ""
DOT         = 100
DASH        = 300
SPACE       = 500

square = np.array( [[1,1,1],[1,1,1],[1,1,1]] )

def parse_cli_args():
    """
    description:
        process commandline arguments, 
        check -h for help 
    """
    # init parses and add arguments
    parser = argparse.ArgumentParser( description="Process arguments" )
    parser.add_argument( '-c', '--crop', nargs=4, \
                         metavar='N', type=int, \
                         help="x y dx dy -> crop image bounded by (x+dx,y+dy)") 
    parser.add_argument( '-e', '--encoding', required=True, \
                         choices=['morse', 'ascii'] )
    parser.add_argument( 'filepath' )

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

    # process arguments and populate relevant flags
    parsed      = parser.parse_args() 
    ENCODING    = parsed.encoding
    FILEPATH    = parsed.filepath
    if( parsed.crop != None ):
        CROP    = True
    return parsed

def main():
    """
    description:
        The driver function
    """
    # open video 
    cap = cv.VideoCapture( FILEPATH )
    logging.debug( "Opening file '%s'" % FILEPATH )
    cv.namedWindow( NAMED_WINDOW, cv.WINDOW_NORMAL )

    # start processing video frame by frame
    while( cap.isOpened() ):
        # get frame and check that it exists
        ret, frame = cap.read()
        if( not ret ):
            print( "cant receive frame" )
            break

        # blur image and pull split channels
        blur = cv.GaussianBlur( frame, (5,5), 0 )
        b,g,r = cv.split( frame )
         
        # pull out rectangle of interest
        rect = g[Y:DY,X:DX]
        print( rect )

        # show
        if( logging.root.level <= logging.DEBUG ):
            cv.imshow( NAMED_WINDOW, rect )
            k = cv.waitKey( 0 )
            if( k == ord( 'q' ) ):
                cv.destroyAllWindows()
                break 
    cap.release()

if( __name__ == "__main__" ):
    args = parse_cli_args()
    logging.basicConfig( level=LOGGING_LEVEL )
    main()
