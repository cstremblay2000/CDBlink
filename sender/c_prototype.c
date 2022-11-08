#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/cdrom.h>

void transmit(){
    int fp;
    int32_t val, num;
    struct cdrom_read r;
    char buffer[2360];

    r.cdread_lba = 1;
    r.cdread_bufaddr = buffer;
    r.cdread_buflen = 2360;
    fp = open("/dev/sr0", O_RDONLY);

    ioctl(fp, CDROMREADRAW, &r);

    printf("Data: %d\n", val );
    close(fp);
}

int main(void){
    printf("Prototype C Transmitter\n");
    transmit();
    return 0;
}
