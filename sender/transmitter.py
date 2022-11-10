from argparse import ArgumentParser
from time import sleep
from subprocess import run

# Global variables for read lengths
short = '500'
long = '1000'


# Convert message to morse code
def morse_encode(msg):

    # Strip non-alphanumeric characters from message
    lower_msg = msg.lower()
    msg = ''
    for i in range(len(lower_msg)): 
        if lower_msg[i].isalnum():
            msg += lower_msg[i]

    # Dictionary for encoding to morse
    morse_dict = {'a': '01', 'b': '1000', 'c': '1010', 'd': '100', 'e': '0', 'f': '0010', 
                'g': '110', 'h': '0000', 'i': '00', 'j': '0111', 'k': '101', 'l': '0100', 
                'm': '11', 'n': '10', 'o': '111', 'p': '0110', 'q': '1101', 'r': '010', 
                's': '000', 't': '1', 'u': '000', 'v': '0001', 'w': '011', 'x': '1001', 
                'y': '1011', 'z': '1100', '0': '11111', '1': '01111', '2': '00111', '3': 
                '00011', '4': '00001', '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110'}

    code = []

    # Convert each char to morse using dictionary
    for c in msg:
        code.append(morse_dict[c])

    # Add sync/calibration signal
    code = '0000' + code + '0000'

    return code


# Encode to binary string for ook and bsfk encoding schemes
def ook_bfsk_encode(msg, codec):
    code = ''

    # Convert input to 7-bit binary
    for char in msg:
        code += str(char.join(format(ord(x), '07b') for x in char))

    # Add sync/calibration signals
    if codec == 2:
        code = '1010101' + code + '1010101'
    else:
        code = '0000' + code + '0000'

    return code


# Transmitter for morse code
def morse_transmit(code):
    log = []

    # Spin up the disk drive
    out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=15', 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1M'], capture_output=True)
    # Save output of dd for log
    log.append(out.stderr.decode().split('\n',2)[2])
    sleep(3)

    # Loop through every char
    for character in code:
        # Loop through each signal for a char
        for signal in character:
            if signal == '0':
                # Transmit dot   
                out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=' + short, 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1K'], capture_output=True)
                log.append(out.stderr.decode().split('\n',2)[2])
            
            else:
                # Transmit dash
                out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=' + long, 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1K'], capture_output=True)
                log.append(out.stderr.decode().split('\n',2)[2])
            
            # Sleep one second between signals
            sleep(1)
            
        # Sleep a total of 3 seconds after finishing a character
        sleep(2)

    # Write output of dd commands to a log file
    f = open('./log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()


# Transmit function for ook encoding
def ook_transmit(code):
    log = []

    # Spin up disk drive
    out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=15', 'iflag=nocache',\
         'oflag=nocache,dsync', 'bs=1M'], capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])
    sleep(5)

    # Read for 1 sec if 1, sleep for 1 if 0
    for bit in code:
        if bit == '0':
            sleep(1)
        else:
            out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=' + short, 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1K'], capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])

    f = open('./log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()


# Transmit function for bsfk encoding
def bsfk_transmit(code):
    log = []

    # Spin up the disk drive
    out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=15', 'iflag=nocache',\
         'oflag=nocache,dsync', 'bs=1M'], capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])
    sleep(5)

    # Read for 1 sec for 0, 2 for 1
    for bit in code:
        if bit == '0':
            out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=' + short, 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1K'], capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])
        else:
            out = run(['dd', 'if=/dev/sr0', 'of=/dev/null', 'count=' + long, 'iflag=nocache',\
                 'oflag=nocache,dsync', 'bs=1K'], capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])
  
        # Sleep one second between signals
        sleep(1)

    f = open('./log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()


# This program uses dd to transmit messages from cd/dvd drives using the access ligth
def main():
    print('CD-Blink Covert Channel Transmitter')

    # Create and parse command line arguments
    parser = ArgumentParser(description='CD-Blink Encoding and Transmission')
    parser.add_argument('-c', '--codec', type=int, required=False, help='Encoding Scheme:\
        1 = Morse(Alphanumeric Only) 2 = On-Off-Keying 3 = Binary Frequency Shift Keying')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--msg', type=str, required=False, help='Message to transmit')
    group.add_argument('-f', '--file', type=str, required=False, help='File to read message from')
    parser.add_argument('-s', '--sblk', type=str, required=False, help='Length in KB of short read')
    parser.add_argument('-l', '--lblk', type=str, required=False, help='Length in KB of long read')
    args = parser.parse_args()

    if args.sblk:
        short = args.sblk
    if args.lblk:
        long = args.lblk

    # Set message to transmit
    if args.msg:
        # Use message provided at command line
        msg = args.msg
    elif args.file:
        # Read message from file
        f = open(args.file, 'r')
        msg = f.read()
        f.close()
    else:
        # Get user input
        msg = input('Enter Mesage to Transmit:\n')

    # Set encoding scheme
    if args.codec:
        encoding_choice = args.codec
    else:
        # User chooses encoding scheme to use
        print('Choose Encoding Scheme')
        print('1 = Morse (Alphanumeric Only)')
        print('2 = On-Off-Keying')
        print('3 = Binary Frequency Shift Keying')
        encoding_choice = int(input(':'))

    # Encode and transmit using scheme users chose
    if encoding_choice == 1:
        code = morse_encode(msg)
        morse_transmit(code)
    elif encoding_choice == 2:
        code = ook_bfsk_encode(msg, 2)
        ook_transmit(code)
    else:
        code = ook_bfsk_encode(msg, 3)
        bsfk_transmit(code)

    print('Complete')


if __name__ == "__main__":
    main()