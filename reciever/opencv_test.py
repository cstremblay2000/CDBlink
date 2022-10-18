import cv2 as cv
import numpy as np
import sys
import logging
import argparse

# debugging and logging constants
NAMED_WINDOW    = "w1"
LOGGING_LEVEL   = logging.DEBUG

# commandline args, constants for cropped
CROP    = False
X1      = 0
Y1      = 0
X2      = 0
Y2      = 0

# commandline args, constance for encoding
ENCODING    = ""
DOT         = 100
DASH        = 300
SPACE       = 500

square = np.array( [[1,1,1],[1,1,1],[1,1,1]] )

def parse_cli_args() -> argparse.Namespace:
    """
    description:
        process commandline arguments, 
        check -h for help 
    returns:
        the namespace created by argparse
    """
    # init parses and add arguments
    parser = argparse.ArgumentParser( description="Process arguments" )
    parser.add_argument( '-c', '--crop', nargs=4, \
                         metavar='N', type=int, \
                         help="x y dx dy -> crop image bounded by (x+dx,y+dy)") 
    parser.add_argument( '-e', '--encoding', required=True, \
                         choices=['morse', 'ascii'] )
    parser.add_argument( 'filepath' )

    # process arguments and populate relevant flags
    parsed      = parser.parse_args() 
    ENCODING    = parsed.encoding
    FILEPATH    = parsed.filepath
    if( parsed.crop != None ):
        CROP    = True
    return parsed

def mahalanobis(x=None, data=None, cov=None):
    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()

def multi_dil(im, num, element=square):
    for i in range(num):
        im = skm.dilation(im, element)
    return im

def multi_ero(im, num, element=square):
    for i in range(num):
        im = skm.erosion(im, element)
    return im

def main():
    # get image and filter noise
    img = cv.imread( args.filepath )
    blur = cv.GaussianBlur( img, (3,3), 0 )
    if( logging.root.level <= logging.DEBUG ):
        cv.imshow("Display window", blur )
        cv.waitKey( 0 )

    # split image into rgb channels
    b, g, r = cv.split( blur )
    if( logging.root.level <= logging.DEBUG ):
        cv.imshow( "Display window", g )
        k = cv.waitKey( 0 )

    # binarize (turn into black and white) the green channel
    ret3,th3 = cv.threshold( g ,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    if( logging.root.level <= logging.DEBUG ):
        cv.imshow( "Display window", th3 )
        k = cv.waitKey( 0 )

    # connected component analysis
    connectivity = 4 
    output = cv.connectedComponentsWithStats( th3, connectivity, cv.CV_32S )
    logging.debug( output[1] )

    # detect edges 
    edged = cv.Canny(th3, 30, 200)
    contours, hierarchy = cv.findContours( edged,
    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours( img, contours, -1, (0,255,0), 3 )
    if( logging.root.level <= logging.DEBUG ):
        cv.imshow( "edges", edged )
        cv.waitKey( 0 )
        cv.imshow( 'Contours', img )
        cv.waitKey( 0 )

    # open video 
    cv.destroyAllWindows()
    cap = cv.VideoCapture( VIDEO_PATH )
    cv.namedWindow( NAMED_WINDOW, cv.WINDOW_NORMAL )
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
        rect = g[Y1:Y2,X1:X2]
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
