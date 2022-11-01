"""
file:       decoders.py
language:   Python3
author:     Chris Tremblay <cst1465@rit.edu>
date:       11/01/2022, National Cook For Your Pets Day!
description:
    Decodes the results from receiver.py in either morse or ascii
"""

# Morse constants
MORSE_DOT   = 1 # second
MORSE_DASH  = 3 # seconds
MORSE_SPACE_SIGNAL  = 1 # seconds
MORSE_SPACE_LETTERS = 3 # seconds
MORSE_SPACE_WORDS   = 7 # seconds

def decode_ascii( duration_on:list, duration_off: list ) -> str:
    return ""

def classify_morse_dot_dash():
    """
    """
    return

def classify_morse_space():
    """
    """
    return

def decode_morse( duration_on:list, duration_off:list ) -> str:
    """
    description:
        decodes morse code where:
        - a DOT is about 1-1.5s
        - a DASH is about 3s
        - and time between DOTS or DASHES is about a second
    parameters:
        duration_on  -> the list of times where durations of light on
        duration_off -> the list of times where the lights are off
    returns:
        the decoded message
    """
    # load morse dictionary
    # TODO

    # start decoding
    msg = "" 
    letter_buffer = list()
    #for i in range( max( len( duration_on ), len( duration_off) ):
        # calculate distances of the duration on to dot or dash
        #dot_dash = classify_morse_dot_dash()

        # classify space
        # space = classify_morse_space()

        # check if light on was first frame or not
        #
    return msg
