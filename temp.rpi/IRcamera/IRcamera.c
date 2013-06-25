#include <stdio.h>
#include <bcm2835.h>
/*#include <wiringPi.h>*/
#include <stdlib.h>
/*#include <fcntl.h>*/

#define BAUD_RATE 120e3

void initIR();
float readTemp();
void writeBMP();

void writeBMP(){
    printf("In writeBMP\n");
    int w = 3;
    int h = 4;
    unsigned char * img = (unsigned char *)malloc(3*w*h);


    char filename[] = "ofp.bmp";
    char * mode = "w";
    FILE *ofp = fopen(filename, mode);
    int x, y;

    int rowSize = 4 * ((3*w + 3)/4);
    // how many bytes in the row (used to create padding)
    int fileSize = 54 + h*rowSize;
    // headers (54 bytes) + pixel data

    for (x=0; x<w; x++){
        for (y=0; y<h; y++){
            int colorVal = 155;
            img[(y*w + x)*3+0] = (unsigned char)colorVal;
        }
    }
    printf("After the for-loop\n");

    unsigned char * bmpPad = (unsigned char *)malloc(sizeof(unsigned char) * (rowSize - 3*w));
    for (int i=0; i<rowSize-3*w; i++) {                 
        bmpPad[i] = 0;
    }

    unsigned char bmpFileHeader[14] = {
        // file header (always starts with BM!)
        'B','M', 0,0,0,0, 0,0, 0,0, 54,0,0,0     };
    unsigned char bmpInfoHeader[40] = {
        // info about the file (size, etc)
        40,0,0,0, 0,0,0,0, 0,0,0,0, 1,0, 24,0     };

    bmpFileHeader[ 2] = (unsigned char)(fileSize);
    bmpFileHeader[ 3] = (unsigned char)(fileSize >>  8);
    bmpFileHeader[ 4] = (unsigned char)(fileSize >> 16);
    bmpFileHeader[ 5] = (unsigned char)(fileSize >> 24);

    bmpInfoHeader[ 4] = (unsigned char)(w);
    bmpInfoHeader[ 5] = (unsigned char)(w >>  8);
    bmpInfoHeader[ 6] = (unsigned char)(w >> 16);
    bmpInfoHeader[ 7] = (unsigned char)(w >> 24);
    bmpInfoHeader[ 8] = (unsigned char)(h);
    bmpInfoHeader[ 9] = (unsigned char)(h >> 8);
    bmpInfoHeader[10] = (unsigned char)(h >> 16);
    bmpInfoHeader[11] = (unsigned char)(h >> 24);

    fprintf(ofp, bmpFileHeader, sizeof(bmpFileHeader));
    fprintf(ofp, bmpInfoHeader, sizeof(bmpInfoHeader));
    fflush(ofp);

    for (int i=0; i<h; i++){
        fprintf(ofp, img+(w*(h-i-1)*3), 3*w);
        fprintf(ofp, bmpPad, (4-(w*3)%4)%4);
        fflush(ofp);
    }




    fflush(ofp);
    
    fclose(ofp);
}

void main(int argc, char **argv){
    float temp, test;

    initIR();
    temp = readTemp();

    printf("%f \n", temp);
    printf("In main\n");
    writeBMP();
    printf("After writeBMP\n");
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

