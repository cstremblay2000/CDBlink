"""
file:       decoders.py
language:   Python3
author:     Chris Tremblay <cst1465@rit.edu>
date:       11/01/2022, National Cook For Your Pets Day!
description:
    Decodes the results from receiver.py in either morse or ascii
"""

from enum import Enum

# shared constants
SPIN_UP_TIME_THRESH = 10
OOK_MANCH_ADJUSTMENT = 1.2 # seconds per blink, should be one, but oh well

# Morse time constants
MORSE_DOT           = 1 # second
MORSE_DASH          = 3 # seconds
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

# morse test data says hello
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

# ASCII encoding constants
OOK_BFSK_PRE_POST_SYNC = '1010101'
MANCHESTER_DECODE_SYNC = '1001100110011001100110011001'

# ASCII test data
A_TEST_ON = [16.398103329009942, 1.4331675673728201, 1.1998612191958495, 
             1.2331906975068454, 2.2997340034587115, 3.332947831099582, 
             1.5664854806168036, 2.166416090214728, 2.1330866119037326, 
             1.266520175817841, 1.3665086107508286, 1.4331675673728201]

A_TEST_OFF = [0.0, 0.6665895662199164, 0.6332600879089205, 0.6999190445309122, 
              0.6665895662199164, 3.5662541792765525, 2.366392960080703, 
              0.366624261420954, 2.7330172215016573, 0.6999190445309122, 
              0.6332600879089205, 0.5666011312869289]

# on off key test data
A_TEST_ON_1 = [16.933333333333334, 1.2, 1.2666666666666667, 1.2333333333333334, 
               3.933333333333333, 1.2333333333333334, 2.7333333333333334, 
               1.2666666666666667, 3.933333333333333, 2.7333333333333334, 
               2.7666666666666666, 2.7, 2.7666666666666666, 6.3, 
               1.2666666666666667, 1.2333333333333334, 1.2333333333333334]

A_TEST_OFF_1 = [1.8666666666666667, 4.766666666666667, 0.6666666666666666, 
                0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 
                2.7, 1.6666666666666667, 0.6333333333333333, 
                0.6666666666666666, 1.6666666666666667, 0.6666666666666666, 
                1.6666666666666667, 0.6666666666666666, 0.6666666666666666, 
                0.6666666666666666, 0.6666666666666666]

#manchester encoding test data
A_TEST_ON_2 = [15.333333333333334, 3.033333333333333, 1.5666666666666667, 
               3.1333333333333333, 1.5666666666666667, 3.066666666666667, 
               1.6, 3.1, 3.1333333333333333, 3.1333333333333333, 
               1.5666666666666667, 1.5333333333333334, 1.5666666666666667, 
               1.5666666666666667, 3.066666666666667, 3.1, 3.1333333333333333, 
               1.6, 1.5, 1.5666666666666667, 3.1, 1.5666666666666667, 3.1, 
               3.1333333333333333, 1.5666666666666667, 1.5666666666666667, 
               1.5333333333333334, 3.066666666666667, 3.1333333333333333, 
               3.1333333333333333, 1.5666666666666667, 3.1, 1.6, 
               3.066666666666667, 1.5666666666666667, 3.1333333333333333]

A_TEST_OFF_2 = [0.7666666666666667, 4.733333333333333, 0.6666666666666666, 
                0.6333333333333333, 0.6333333333333333, 0.6666666666666666, 
                0.6666666666666666, 0.6333333333333333, 0.6333333333333333, 
                0.6666666666666666, 0.6333333333333333, 0.6666666666666666, 
                0.6666666666666666, 0.6333333333333333, 0.6666666666666666, 
                0.6666666666666666, 0.6333333333333333, 0.6333333333333333, 
                0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 
                0.6333333333333333, 0.6666666666666666, 0.6333333333333333, 
                0.6666666666666666, 0.6333333333333333, 0.6666666666666666, 
                0.6666666666666666, 0.6666666666666666, 0.6333333333333333, 
                0.6666666666666666, 0.6666666666666666, 0.6333333333333333, 
                0.6666666666666666, 0.6666666666666666, 0.6333333333333333]

def ook_manchester_demodulate( dur_on:list, dur_off:list, lff:bool ) -> str:
    """
    description:
        demodulates a list of durations into a bitstring
        using on-off-keying (ook) or manchester encoding
        note, the time that a light is on might not actually be closer
        to 1.2-1.5 seconds when it should be one. there is a compensation
        mechanism in the for first for loop that accomodats for that
    parameters:
        dur_on  -> the list of durations the light is on for
        dur_off -> the list of durations the light is off for
        lff     -> if the light is on for the first frame (light first frame)
    returns:
        a string containing ascii 1's and 0's
    """
    # init local vars
    bitstring_on = list()
    bitstring_off = list()
    bitstring = ''

    # classify bits on 
    for dur in dur_on:
        num_bits = round( dur/OOK_MANCH_ADJUSTMENT ) # actual time is ~1.2-1.5s
        if( num_bits == 0 ):
            num_bits = 1
        bitstring_on.append( '1'*num_bits )

    for dur in dur_off:
        num_bits = round( dur )
        if( num_bits == 0 ):
            num_bits = 1
        bitstring_off.append( '0'*num_bits )

    # join bit string, start at one to skip spin up time
    idx_on = 1
    idx_off = 1
    on = ''
    off = ''
    ldon = len( bitstring_on )
    ldoff = len( bitstring_off )
    while( True ):
        # check if still looping
        if( idx_on >= ldon and idx_off >= ldoff ):
            break

        # if in bounds get element
        if( idx_on < ldon ):
            on = bitstring_on[idx_on]
            idx_on += 1
        if( idx_off < ldoff ):
            if( idx_off == 1 ):
                off = '' # skip 5s wait
            else:
                off = bitstring_off[idx_off]
            idx_off += 1

        # assemble bitstring in corret order if light was on first
        if( lff ):
            bitstring += on + off
        else:
            bitstring += off + on
        
    return bitstring

def ook_bfsk_decode( bitstring:str ) -> str:
    """
    description:
        decodes a bitstring if it has been demodulated from 
        on-off-keying (ook) or binary frequency shift keying (bfsk)
    parameters:
        bitstring -> the ascii string containing 1's and 0's
    returns:
        the decoded message
    """
    # create 7 bit substrings 
    substrings = [bitstring[i:i+7] for i in range( 0, len(bitstring), 7 )]

    # decode message
    msg = ""
    for ss in substrings:
        if( ss == OOK_BFSK_PRE_POST_SYNC ):
            continue
        else:
            msg += chr( int( ss, 2 ) ) 
    return msg

def manchester_decode( bitstring:str ) -> str:
    """
    description:
        decodes a string that uses machester encoding
        01 encodes a 0 
        10 encodes a 1
    parameters:
        bitstring -> the bit string that needs to be decoded
    returns:
        the decoded message
    """
    msg = ""

    substrings = bitstring.split( MANCHESTER_DECODE_SYNC )
    for ss in substrings:
        print( ss )
    return ""

def decode_ascii( dur_on:list, dur_off: list, encoding:int, lff:bool ) -> str:
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
        # for sync messages, probably a better way to do this but oh well
        if( dur_on[i] > SPIN_UP_TIME_THRESH ):
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
    print( "morse test" )
    msg = decode_morse( TEST_ON, TEST_OFF, False )
    print( "\t", msg )
    print( "done" )
    print()

    # decode ascii
    print( "ascii test" )
    print( "\t", "ook test, expecting hello" )
    bs = ook_manchester_demodulate( A_TEST_ON_1, A_TEST_OFF_1, False )
    print( "\t","demodulated", len( bs ), "bits" , bs )

    msg = ook_bfsk_decode( bs )
    print( "\t", "decoded", msg )
    print()

    print( "\t", "manchester test, expecting abc" )
    print( "\t", "not implemented yet" )
    print( )

    print( "\t", "bfsk test, expecting abc" )
    print( "\t", "not implemented yet" )
    print( "done" )
    return

if( __name__ == "__main__" ):
    main()
