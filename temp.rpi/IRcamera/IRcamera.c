#include <stdio.h>
#include <bcm2835.h>
/*#include <stdlib.h>*/
/*#include <fcntl.h>*/
#define BAUD_RATE 120e3

void initIR();
float readTemp();
float main(int argc, char **argv){
    float temp, test;

    initIR();
    for (int i=0; i<1e2; i++){
        temp = readTemp();
        if (i==4) test = readTemp();
    }
    printf("%f\n", test);

    return (float)temp;
}

float readTemp(){
    // adapted from  http://www.raspberrypi.org/phpBB3/viewtopic.php?t=17738&p=362569
    unsigned char i,reg;
    reg = 0x07; // it reads from RAM 0x07
    unsigned char buf[6];
    double temp=0;

    bcm2835_i2c_begin();
    bcm2835_i2c_write(&reg, 1);
    bcm2835_i2c_read_register_rs(&reg,&buf[0],3);

    temp = (double) (((buf[1]) << 8) + buf[0]);
    temp = (temp * 0.02)-0.00;
    temp = temp - 273.15;
    return (float)temp;

}
void initIR(){
    bcm2835_init();
    bcm2835_i2c_begin();
    bcm2835_i2c_set_baudrate((int)BAUD_RATE);
    bcm2835_i2c_setSlaveAddress(0x5a);
}
