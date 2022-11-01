#include <stdio.h>
#include <linux/ioctl.h>

void transmit(){
    int buffer;
    FILE *fp;
    fp = fopen("/dev/sr0", "r");

    fread(&buffer, sizeof(int), 1, fp);
}

int main(void){
    printf("Prototype C Transmitter\n");
    transmit();
    return 0;
}