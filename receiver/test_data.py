#!/usr/bin/env python
"""
file:       test_data.py
author:     Chris Tremblay <cst1465@rit.edu>
language:   Python3
date:       11/10/2022
description:
    some test data for the decoders
"""

# morse test on 
# this was created by had so it is idea data
MORSE_HELLO_ONE_S_ON  = [22,1,      # start up cylce and calibration
                         1,1,1,1,   # h
                         1,         # e
                         1,3,1,1,   # l
                         1,3,1,1,   # l
                         3,3,3,     # 0
                         12]        # end of transmision
MORSE_HELLO_ONE_S_OFF = [0.8,1,1,
                         1,1,1,3,
                         3,
                         1,1,1,3,
                         1,1,1,3,
                         1,1,3]

# morse test 
# this was created by hand so it is idea
MORSE_HELLO_HALF_S_ON  = [22,0.5,           # start up cylce and calibration
                         0.4,0.4,0.5,0.5,   # h
                         0.5,               # e
                         0.5,1.6,0.45,0.45, # l
                         0.5,1.4,0.5,0.5,   # l
                         1.5,1.6,1.4,       # 0
                         12]                # end of transmision
MORSE_HELLO_HALF_S_OFF = [0.8,0.5,0.5,
                         0.5,0.5,0.5,1.5,
                         1.5,
                         0.5,0.5,0.5,1.5,
                         0.5,0.5,0.5,1.5,
                         0.5,0.5,1.5]

# ook test 
# created by hand so it is ideal
OOK_HELLO_ONE_S_ON  = [22,1,2,1,2,1,3,2,2,2,2,4] 
 
OOK_HELLO_ONE_S_OFF = [0.8,1,1,1,3,2,1,1,2,1,2,1]

# ook test
# this was created by hand so it is ideal
OOK_HELLO_HALF_S_ON  = [22,0.5,1,0.5,1,0.5,1.5,1,1,1,1,2]

OOK_HELLO_HALF_S_OFF = [0.8,1,1,0.5,1.5,1,0.5,0.5,1,0.5,1,0.5]

# bfsk test 
# created by hand so it's ideal
BFSK_HELLO_ONE_S_ON  = [22,1,2,2,1,2,1,1,1,2,2,1,1,2,1,2,2,2,1,2,2,1,1,2,2,1,2,2,1,1,2,2,1,2,2,2,2]
BFSK_HELLO_ONE_S_OFF = [0.8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# bfsk test 
# created by hand so it is ideal
BFSK_HELLO_HALF_S_ON  = [22,0.5,1,1,0.5,1,0.5,0.5,0.5,1,1,0.5,0.5,1,0.5,1,1,1,0.5,1,1,0.5,0.5,1,1,0.5,1,1,0.5,0.5,1,1,0.5,1,1,1,1]
BFSK_HELLO_HALF_S_OFF = [0.8,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

