from time import sleep
import subprocess


def user_input():
    print('Non-alphanumeric characters will be stripped')
    raw = input("Enter message to encode:")
    
    raw = raw.lower()
    message = ''
    for i in range(len(raw)): 
        if raw[i].isalnum():
            message += raw[i]

    return message


def encode(message):
    f = open('./sender/morse_code.txt', 'r')
    lines = f.readlines()

    code = ''
    for c in message:
        for line in lines:
            if line[0] == c:
                code += line[2:]
                code = code.strip()
    
    f.close()

    return code


def transmit(code):
    sync = 15
    dot = 1
    dash = 3
    log = []

    out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(sync) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])

    for signal in code:
        if signal == '0':
            out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(dot) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])
        else:
            out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(dash) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
            log.append(out.stderr.decode().split('\n',2)[2])

        sleep(1)
    
    out = subprocess.run('dd if=/dev/sr0 of=/dev/null count=' + str(sync) + ' iflag=nocache oflag=nocache,dsync bs=1M ', shell=True, capture_output=True)
    log.append(out.stderr.decode().split('\n',2)[2])

    f = open('./sender/log.txt', 'w')
    for line in log:
        f.write(line)
    f.close()


def main():
    print('CD-Blink Morse Code Transmitter')
    message = user_input()
    code = encode(message)
    transmit(code)
    print('Complete')


if __name__ == "__main__":
    main()