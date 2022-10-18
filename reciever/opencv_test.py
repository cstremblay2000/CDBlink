import cv2 as cv
import numpy as np
import sys
import logging

VIDEO_PATH="./images/test.mp4"
NAMED_WINDOW="w1"

square = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]])

def init_logging():
    logging.basicConfig( level=logging.DEBUG )
    return 

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
    # initialize logging
    init_logging()

    # get image and filter noise
    img = cv.imread( sys.argv[1] )
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
    cap = cv.VideoCapture( VIDEO_PATH )
    cv.namedWindow( NAMED_WINDOW, cv.WINDOW_NORMAL )
    while( cap.isOpened() ):
        ret, frame = cap.read()
        if( not ret ):
            print( "cant receive frame" )
            break
        
        gray = cv.cvtColor( frame, cv.COLOR_BGR2GRAY )
        if( logging.root.level <= logging.DEBUG ):
            cv.imshow( NAMED_WINDOW, gray )
            cv.waitKey( 0 )
    cap.release()

if( __name__ == "__main__" ):
    main()
