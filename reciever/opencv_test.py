import cv2 as cv
import numpy as np
import sys

square = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]])

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
    img = cv.imread( sys.argv[1] )
    blur = cv.GaussianBlur( img, (3,3), 0 )
    cv.imshow("Display window", blur )
    k = cv.waitKey( 0 )

    # split image into rgb channels
    b, g, r = cv.split( blur )
    cv.imshow( "Display window", g )
    k = cv.waitKey( 0 )

    # binarize (turn into black and white) the green channel
    ret3,th3 = cv.threshold( g ,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imshow( "Display window", th3 )
    k = cv.waitKey( 0 )

    # connected component analysis
    connectivity = 4 
    output = cv.connectedComponentsWithStats( th3, connectivity, cv.CV_32S )
    print( output[1] )

    # detect edges 
    edged = cv.Canny(th3, 30, 200)
    cv.imshow( "edges", edged )
    contours, hierarchy = cv.findContours( edged,
    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours( img, contours, -1, (0,255,0), 3 )
    cv.imshow( 'Contours', img )
    cv.waitKey( 0 )

if( __name__ == "__main__" ):
    main()
