"""
file:       decoders.py
language:   Python3
author:     Chris Tremblay <cst1465@rit.edu>
date:       11/01/2022, National Cook For Your Pets Day!
description:
    Decodes the results from receiver.py in either morse or ascii
"""

from enum import Enum

# Morse time constants
MORSE_DOT   = 1 # second
MORSE_DASH  = 3 # seconds
MORSE_SPACE_SIGNAL  = 1 # seconds
MORSE_SPACE_LETTER  = 3 # seconds
MORSE_SPACE_WORD    = 7 # seconds

# Enums
SPACES = Enum( 'MorseSpaces', ['SIGNAL','LETTER', 'WORD' ] )

# morse dictionary 
MORSE_DICT = {'01': 'a', '1000': 'b', '1010': 'c', '100': 'd', '0': 'e', 
              '0010': 'f', '110': 'g', '0000': 'h', '00': 'i', '0111': 'j', 
              '101': 'k', '0100': 'l', '11': 'm', '10': 'n', '111': 'o', 
              '0110': 'p', '1101': 'q', '010': 'r', '000': 's', '1': 't', 
              '001': 'u', '0001': 'v', '011': 'w', '1001': 'x', '1011': 'y', 
              '1100': 'z', '11111': '0', '01111': '1', '001111': '2', 
              '00011': '3', '00001': '4', '00000': '5', '10000': '6', 
              '11000': '7', '11100': '8', '11110': '9'}

# test date says hello
TEST_ON=[22.233333333333334, 1.5, 1.5, 1.5333333333333334, 1.5666666666666667, \
         1.5333333333333334, 1.5333333333333334, 3.1, 1.5666666666666667, \
         1.5333333333333334, 1.5666666666666667, 3.066666666666667, \
         1.5666666666666667, 1.5333333333333334, 3.1, 3.066666666666667, \
         3.1, 12.166666666666666]

TEST_OFF=[0.8666666666666667, 0.6666666666666666, 0.7, 0.6666666666666666, \
          0.6666666666666666, 2.8666666666666666, 2.8666666666666666, \
          0.6666666666666666, 0.6666666666666666, 0.6666666666666666, \
          2.8666666666666666, 0.6666666666666666, 0.6666666666666666, \
          0.6666666666666666, 2.8666666666666666, 0.6666666666666666, \
          0.6666666666666666, 0.6]

def decode_ascii( duration_on:list, duration_off: list ) -> str:
    """
    """
    # TODO
    return ""

def classify_morse_dot_dash( duration:int ) -> chr:
    """
    description:
        classfies whether a duraction on is a dot or dash
    parameters:
        duration -> the duration light is on
    returns:
        '0' -> character zero if a dot
        '1' -> character one if a dash
    """
    # get distances
    dist_dot  = abs( duration - MORSE_DOT )
    dist_dash = abs( duration - MORSE_DASH )

    # classify
    min_dist = min( dist_dot, dist_dash )
    
    if( min_dist == dist_dot ):
        return '0'
    if( min_dist == dist_dash ):
        return '1'
    return None

def classify_morse_space( duration:int ) -> Enum:
    """
    description:
        classifies the duration the time was off to determin
        whether a word, letter, or dot/dash is being deliniated
    paraemeters:
        duraction -> the duration the light was off for
    returns:
        SPACES.SIGNAL -> if space between signals
        SPACES.LETTER -> if space between letters
        SPACES.WORD   -> if space between words
    """
    # get distances 
    sig_dist = abs( duration - MORSE_SPACE_SIGNAL )
    let_dist = abs( duration - MORSE_SPACE_LETTER )
    wor_dist = abs( duration - MORSE_SPACE_WORD   )

    # calc min distance
    min_dist = min( sig_dist, let_dist, wor_dist )

    # classify
    if( min_dist == sig_dist ):
        return SPACES.SIGNAL
    if( min_dist == let_dist ):
        return SPACES.LETTER
    if( min_dist == wor_dist ):
        return SPACES.WORD
    return None

def decode_morse( dur_on:list, dur_off:list, light_first_frame:bool  ) -> str:
    """
    description:
        decodes morse code where:
        - a DOT is about 1-1.5s
        - a DASH is about 3s
        - and time between DOTS or DASHES is about a second
    parameters:
        dur_on  -> the list of times where durations of light on
        dur_off -> the list of times where the lights are off
        light_first_frame -> if the light was on for the first frame
    returns:
        the decoded message
    """
    # start decoding
    msg = "" 
    buffer = ""
    for i in range( 1, max( len( dur_on ), len( dur_off ) ) ):
        # for sync messages
        if( dur_on[i] > 10 ):
            continue 

        # calculate distances of the duration on to dot or dash
        dot_dash = classify_morse_dot_dash( dur_on[i] )

        # classify space
        space = classify_morse_space( dur_off[i] )

        # check if light on was first frame or not
        if( space == SPACES.SIGNAL or buffer == "" ):
            buffer += dot_dash
        if( space == SPACES.LETTER ):
            msg += MORSE_DICT[buffer]
            buffer = dot_dash
        if( space == SPACES.WORD ):
            msg += MORSE_DICT[buffer]
            buffer = dot_dash

    if( buffer != "" and buffer in MORSE_DICT.keys() ):
        msg += MORSE_DICT[buffer]
    return msg

def main():
    """
    description:
        little test suite
    """
    # decode morse
    msg = decode_morse( TEST_ON, TEST_OFF, False )
    print( msg )

    return

if( __name__ == "__main__" ):
    main()
