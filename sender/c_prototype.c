#include <stdio.h>
#include <linux/ioctl.h>

void transmit(){
    int buffer[1024];
    FILE *fp;
    fp = open("/dev/sr0", "r");
    setvbuf(fp, NULL, _IONBF, 0);

    read(&buffer, sizeof(buffer), 1024, fp);
    fclose(fp);
}

int main(void){
    printf("Prototype C Transmitter\n");
    transmit();
    return 0;
}