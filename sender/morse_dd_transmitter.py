from time import sleep
import subprocess


# Get user input and strip special chars
def user_input():
    # Get message
    print('Non-alphanumeric characters will be stripped')
    raw = input("Enter message to encode:")
    
    # Strip special chars
    raw = raw.lower()
    message = ''
    for i in range(len(raw)): 
        if raw[i].isalnum():
            message += raw[i]

    return message


# Convert message to morse code
def encode(message):
    # Read code file
    f = open('./sender/morse_code.txt', 'r')
    lines = f.readlines()

    code = []
    encoded_char = ''

    # Convert each char to morse
    for c in message:
        # Look through lines of code file for character
        for line in lines:
            if line[0] == c:
                encoded_char += line[2:]
                encoded_char = encoded_char.strip()
        code.append(encoded_char)
        encoded_char = ''
    
    f.close()

    return code


# Transmit the message
def transmit(code):
    sync = 15
    dot = 1
    dash = 3
    log = []

    # Sync signal/spin up the disk drive
    out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(sync) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])
    sleep(2)

    # Loop through every char
    for character in code:
        # Loop through each signal for a char
        for signal in character:
            # Transmit dot
            if signal == '0':
                out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(dot) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
                log.append(out.stderr.decode().split('\n',2)[2])
            else:
                # Transmit dash
                out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(dash) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
                log.append(out.stderr.decode().split('\n',2)[2])
            
            # Sleep one second between signals
            sleep(1)
        # Sleep a total of 3 seconds after finishing a character
        sleep(2)
    
    # Sync signal, message done
    out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(sync) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])

    # Write output of dd commands to a log file
    f = open('./sender/log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()


# This program uses dd to transmit morse code via cd/dvd drive led lights 
def main():
    print('CD-Blink Morse Code Transmitter')
    message = user_input()
    code = encode(message)
    transmit(code)
    print('Complete')


if __name__ == "__main__":
    main()