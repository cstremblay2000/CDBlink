#!/usr/bin/env python
"""
file:       decoders.py
language:   Python3
author:     Chris Tremblay <cst1465@rit.edu>
date:       11/01/2022, National Cook For Your Pets Day!
description:
    Decodes the results from receiver.py in either morse or ascii
    The reciever is designed to have one large blink at the beginning
    and then a calibration blink right after that lets the the decoder know
    how long the blink are going to be
"""

from enum import Enum
from statistics import mean

# shared constants
SPIN_UP_TIME_THRESH     = 10 # seconds

# Morse time constants
MORSE_DOT           = 1 
MORSE_DASH          = 3 
MORSE_SPACE_SIGNAL  = 1
MORSE_SPACE_LETTER  = 3 
MORSE_SPACE_WORD    = 7

# ASCII encoding constants
OOK_BFSK_PRE_POST_SYNC = '1010101'

# bfsk constants
BFSK_ZERO   = 1
BFSK_ONE    = 2 

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

def ook_demodulate( dur_on:list, dur_off:list ) -> str:
    """
    description:
        Demodulats on-on-keying based on durations provided by user.
        It is structed by having one large blink to ensure that the disk is
        spun up. then a calibration blink is sent so that the decoder
        knows how long a blink is going to be. that caliration blink
        will be used to know how long something is on/off
    parameters:
        dur_on  -> the list of durations the light is on for
        dur_off -> the list of durations the light is off for
    returns:
        a string containing ascii 1's and 0's
    """
    # init local vars
    bitstring_on = list()
    bitstring_off = list()
    bitstring = ''

    # get calibration blink
    calibration_blink = dur_on[1]
    calibration_blink_on = mean( dur_on[1:5] )
    calibration_blink_off = mean( dur_off[2:5] )
    print( "calibration blink", calibration_blink )

    # classify bits on 
    for dur in dur_on[2:]:
        num_bits = round( dur/calibration_blink_on )
        print( "duron %f, num bits %d, calibrate blink %f" % 
                (dur, num_bits, calibration_blink_on ) )
        if( num_bits == 0 ):
            num_bits = 1
        bitstring_on.append( '1'*num_bits )

    for dur in dur_off[3:]:
        num_bits = round( dur/calibration_blink_off )
        print( "duroff %f, num bits %d calibrate blink %f" % 
               (dur, num_bits, calibration_blink_off ) )
        if( num_bits == 0 ):
            num_bits = 1
        bitstring_off.append( '0'*num_bits )

    # join bit string, start at one to skip spin up time
    idx_on = 0
    idx_off = 0
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
        else:
            on = ""
        if( idx_off < ldoff ):
            off = bitstring_off[idx_off]
            idx_off += 1
        else:
            off = ""

        # assemble bitstring in corret order if light was on first
        bitstring += on + off
        
    return bitstring

def bfsk_demodulate( dur_on:list, dur_off:list ) -> str:
    """
    desription:
        demodulates a binary frequency shift keying modulated message.
        The first blink is very long and ensures that the the drive is spun up
        Then a calibration link is sent to get how long a zero duration is for.
        The time will be double for a one. 
    parameters:
        dur_on  -> the list of times light was on
        dur_off -> the list of times the light was off
    returns:
        the demodulated bit string
    """
    # init some stuff
    idx_on = 2
    ldon = len( dur_on )
    on = 0
    bitstring = ''
    calibration_blink = dur_on[1]
    while( True ):
        # check if we should still be looping
        if( idx_on >= ldon ):
            break

        # get duration on
        on = dur_on[idx_on]

        # calculate distances from 1 second to 2 second
        dist_zero = abs( on/calibration_blink - BFSK_ZERO )
        dist_one  = abs( on/calibration_blink - BFSK_ONE )

        # classify
        if( min( dist_zero, dist_one ) == dist_zero ):
            bitstring += '0'
        else:
            bitstring += '1'
        idx_on += 1

    return bitstring

def bfsk_decode( dur_on:list, dur_off:list ) -> str:
    """
    description:
        decodes a bitstring if it has been demodulated from 
        on-off-keying (ook) or binary frequency shift keying (bfsk)
    parameters:
        bitstring -> the ascii string containing 1's and 0's
    returns:
        the decoded message
    """
    # demodulate string
    bitstring = bfsk_demodulate( dur_on, dur_off )
    print( len( bitstring ), bitstring )

    # create 7 bit substrings 
    substrings = [bitstring[i:i+7] for i in range( 0, len(bitstring), 7 )]
    
    # decode message
    msg = ""
    for ss in substrings:
        if( len( ss ) < 7 ):
            ss = ss + '0'*(7-len(ss)) # pad with zeros 
        print( len( ss ), ss )
        msg += chr( int( ss, 2 ) ) 
    return msg

def ook_decode( dur_on:list, dur_off:list ) -> str:
    """
    description:
        decodes a bitstring if it has been demodulated from 
        on-off-keying (ook) or binary frequency shift keying (bfsk)
    parameters:
        bitstring -> the ascii string containing 1's and 0's
    returns:
        the decoded message
    """
    # demodulate ook
    bitstring = ook_demodulate( dur_on, dur_off )
    ( len( bitstring), bitstring )

    # create 7 bit substrings 
    substrings = [bitstring[i:i+7] for i in range( 0, len(bitstring), 7 )]

    # decode message
    msg = ""
    for ss in substrings:
        if( len( ss ) < 7 ):
            ss = ss + '0'*(7-len(ss)) # pad last substring with zeros
        print( len(ss), ss )
        msg += chr( int( ss, 2 ) )
    return msg

def classify_morse_dot_dash( duration:int, cb:float ) -> chr:
    """
    description:
        classfies whether a duraction on is a dot or dash
    parameters:
        duration -> the duration light is on
        cb       -> the calibration blink
    returns:
        '0' -> character zero if a dot
        '1' -> character one if a dash
    """
    # get distances
    dist_dot  = abs( duration/cb - MORSE_DOT )
    dist_dash = abs( duration/cb - MORSE_DASH )

    # classify
    min_dist = min( dist_dot, dist_dash )
    
    if( min_dist == dist_dot ):
        return '0'
    if( min_dist == dist_dash ):
        return '1'
    return None

def classify_morse_space( duration:int, cb:float ) -> Enum:
    """
    description:
        classifies the duration the time was off to determin
        whether a word, letter, or dot/dash is being deliniated
    paraemeters:
        duraction -> the duration the light was off for
        cb        -> the calibration blink
    returns:
        SPACES.SIGNAL -> if space between signals
        SPACES.LETTER -> if space between letters
        SPACES.WORD   -> if space between words
    """
    # get distances 
    sig_dist = abs( duration/cb - MORSE_SPACE_SIGNAL )
    let_dist = abs( duration/cb - MORSE_SPACE_LETTER )
    wor_dist = abs( duration/cb - MORSE_SPACE_WORD )

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

def decode_morse( dur_on:list, dur_off:list  ) -> str:
    """
    description:
        A long blink is first sent to ensure that the drive is spun up.
        Then a calibration blink is sent to represent one unit for morse

        the morse will then be decoded where:
            - a DOT is ONE unit
            - a DASH is THREE units
            - SPACE between SIGNALS is ONE unit
            - SPACE between LETTERS is THREE units
            - SPACE between WORDS is 7 UNITS
    parameters:
        dur_on  -> the list of times where durations of light on
        dur_off -> the list of times where the lights are off
    returns:
        the decoded message
    """
    # start decoding
    msg = "" 
    buffer = ""
    calibration_blink = -1
    for i in range( 1, max( len( dur_on ), len( dur_off ) ) ):
        # for sync messages, probably a better way to do this but oh well
        if( dur_on[i] > SPIN_UP_TIME_THRESH ):
            continue 

        # read the calibration blink
        if( i == 1 ):
            calibration_blink = dur_on[i]
            continue

        # calculate distances of the duration on to dot or dash
        dot_dash = classify_morse_dot_dash( dur_on[i], calibration_blink )

        # classify space
        space = classify_morse_space( dur_off[i], calibration_blink )

        # check if light on was first frame or not
        try:
            if( space == SPACES.SIGNAL or buffer == "" ):
                buffer += dot_dash
                print( "\t", dot_dash )
            if( space == SPACES.LETTER ):
                msg += MORSE_DICT[buffer]
                buffer = dot_dash
                print( "detected letter", msg )
                print( "\t", buffer )
            if( space == SPACES.WORD ):
                msg += ' ' + MORSE_DICT[buffer]
                buffer = dot_dash
                print( "detected word", msg )
                print( "\t", buffer )
        except Exception as e:
            msg += '_'
            buffer = dot_dash
            print( e )

    if( buffer != "" and buffer in MORSE_DICT.keys() ):
        msg += MORSE_DICT[buffer]
    return msg

def main():
    """
    description:
        little test suite, might error there was a time crunch
    """
    # conditional import to avoid loading test data when file
    # is being used as a library
    import test_data as td

    # decode morse
    print( "morse test, expecting result: hello" )
    msg = decode_morse( td.MORSE_HELLO_ONE_S_ON, 
                        td.MORSE_HELLO_ONE_S_OFF )
    print( "\t", "ideal one second test result:", msg )
    msg = decode_morse( td.MORSE_HELLO_HALF_S_ON,
                        td.MORSE_HELLO_HALF_S_OFF )
    print( "\t", "ideal half second test result:", msg )
    print( "done" )
    print()

    # decode ascii
    print( "ascii test, expecting hello" )
    print( "\t", "ook test one second" )
    bs = ook_demodulate( td.OOK_HELLO_ONE_S_ON, 
                         td.OOK_HELLO_ONE_S_OFF )
    print( "\t","demodulated", len( bs ), "bits" , bs )
    msg = ook_bfsk_decode( bs )
    print( "\t", "decoded", msg )
    print()


    print( "ascii test, expecting hello" )
    print( "\t", "ook test half second" )
    bs = ook_demodulate( td.OOK_HELLO_HALF_S_ON,
                         td.OOK_HELLO_HALF_S_OFF )
    print( "\t","demodulated", len( bs ), "bits" , bs )
    msg = ook_bfsk_decode( bs )
    print( "\t", "decoded", msg )
    print()


    print( "\t", "bfsk one second test" )
    bs = bfsk_demodulate( td.BFSK_HELLO_ONE_S_ON,
                         td.BFSK_HELLO_ONE_S_OFF )
    print( "\t","demodulated", len( bs ), "bits" , bs )
    print( "\t", "decoded", msg )
    print()

    print( "\t", "bfsk test half second" )
    bs = bfsk_demodulate( td.BFSK_HELLO_HALF_S_ON,
                          td.BFSK_HELLO_HALF_S_OFF )
    print( "\t","demodulated", len( bs ), "bits" , bs )
    msg = ook_bfsk_decode( bs )
    print( "\t", "decoded", msg )

    print( "done" )
    return

if( __name__ == "__main__" ):
    main()
