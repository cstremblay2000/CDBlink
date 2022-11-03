from time import sleep
import subprocess


# Get user input and convert to binary
def get_message():
    message = input("Enter message to encode:")

    code = ''
    # Convert input to binary, 7-bits
    for char in message:
        code += str(char.join(format(ord(x), '07b') for x in char))

    return code


# Transmit message using dd
def transmit(code):
    log = []
    # Add sync signals to beginning and end of binary sequence
    code = '0101010' + code + '0101010'

    # Spin up disk drive
    out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=15 iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])

    # Transmit data, read for 1 sec if 1, sleep for 1 if 0
    for bit in code:
        if bit == '0':
            sleep(1)
        else:
            out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=1 iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])

    # Write output of dd commands to a log file
    f = open('./log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()

# This program uses dd to transmit data encoded as 7-bit ascii using cd/dvd drive led lights
def main():
    print('CD-Blink Binary Code Transmitter')
    print('Uses 7-Bit ASCII Encoding')
    code = get_message()
    transmit(code)
    print('Complete')


if __name__ == "__main__":
    main()