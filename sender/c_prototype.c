#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/ioctl.h>
#include <linux/cdrom.h>

void transmit(){
    int fp;
    int32_t val, num;
    fp = open("/dev/sr0", O_RDWR);

    ioctl(fp, CDROMREADRAW, 0);

    printf("Data: %d\n", val);
    close(fp);
}

int main(void){
    printf("Prototype C Transmitter\n");
    transmit();
    return 0;
}