/* 
 * All of this code can be found on GitHub, at https://github.com/scottsievert/IRcamera
 *
 * At first, this project used an Arduino and two servos to take a picture. The
 * Arduino only has 2k of RAM and the servos tend me be imprecise, meaning, at
 * maximum, could only get about a 13x10 image out. So, we switched to the
 * Raspberry Pi (512Mb of RAM!) and some stepper motors, which are much more
 * accurate. For development, this choice was also better. I got off the silly
 * Arduino IDE and into Vim, and am closer to bash. Code completion, beautiful
 * syntax highlighting, nice shortcuts... but I could go on all day about Vim.
 *
 * Normal IR cameras, ones that aren't made out of a single sensor, normally
 * cost between 4,000 and 40,000 dollars -- insane expensive.
 *
 * The parts needed are:
 * | Part           | Number | Total Price |
 * |----------------|--------|-------------|
 * | RPi            | 1      | 35          |
 * | IR sensor      | 1      | 35          |
 * | Driver boards  | 2      | 200         |
 * | Stepper motors | 2      | 70          |
 * | Total          |        | 340         |
 *      
 *      - Stepper motors (also in steppers.c):
 *          url: http://www.phidgets.com/products.php?category=23&product_id=3317_1
 *      - Driver boards (also in steppers.c):
 *          url: http://www.phidgets.com/products.php?product_id=1067
 *      - IR sensor: MLX90614 DCI
 *          url: http://www.futureelectronics.com/en/technologies/semiconductors/analog/sensors/temperature/Pages/3003055-MLX90614ESF-DCI-000-TU.aspx?IM=0
 *      - Raspberry Pi:
 *          I'm sure a simple Google search will get you what you want. It's a popular device.
 *
 *  I'm writing good docs because I hate it when there are poor docs.
 *  Absolutely, positively, resoundingly hate it. Probably too much, but oh
 *  well.
 *
 *  --Scott Sievert (sieve121@umn.edu), 2013-06-26
 */



#include <stdio.h>
#include <bcm2835.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>
#include <phidget21.h>
#include "steppers.h"
#include <unistd.h>

#define WIDTH 100
#define HEIGHT 100

#define BAUD_RATE 100e3
#define DEBUG_PRINT 1

#define WAIT_MS 300 // note that the motors (as of 2013-06-27) wait until they're in position
#define SAME_IMAGE_FILE 1

// the constants that determines the width of blue-red
#define A 2.4e-1f
#define CENTER 30.0f
#define K 1.0f // since B taken in RGB
#define E 2.718281828459045f

#define ADDRESS 0x00
#define COMMAND 0x25
#define MSB 0xb1
#define LSB 0x74
#define PEC 0x6b

void initIR();
float readTemp();
void writeBMP(float * in, int w, int h);
void writePPM();
int readConfig();
void writeConfig();
void waitMillis(int millis);

void main(int argc, char **argv){
    int data;
    float temp, temp1;
    int i=0;
    int repeat=0;
    FILE * file = fopen("noise.txt", "w");
    initIR();
    printf("WAIT_MS: %d\n", WAIT_MS);


    while(i < 10){
        i++;
        temp = readTemp();
        waitMillis(WAIT_MS);
        printf( "%f\n", temp);
    }
    
    printf("repeats: %d\n", repeat);


    bcm2835_i2c_end();

        /*printf("Error = %d out of 100\n", error);*/
        /*fromSampleCode();*/
        /*CPhidgetStepperHandle stepper = 0;*/
        /*CPhidgetStepper_create(&stepper);*/

        /*initStepper(stepper);*/
        /*printf("Done with init...\n");*/
        /*fflush(stdout);*/
        /*getchar();*/

        /*gotoPixel2D(stepper, stepper, 0, WIDTH, 0, HEIGHT);*/
        /*gotoPixel2D(stepper, stepper, WIDTH, WIDTH, HEIGHT, HEIGHT);*/
        /*gotoPixel2D(stepper, stepper, 0, WIDTH, 0, HEIGHT);*/
        /*gotoPixel2D(stepper, stepper, WIDTH, WIDTH, HEIGHT, HEIGHT);*/
        /*gotoPixel2D(stepper, stepper, 0, WIDTH, 0, HEIGHT);*/
        /*gotoPixel2D(stepper, stepper, WIDTH, WIDTH, HEIGHT, HEIGHT);*/


        /*haltStepper(stepper);*/

        /*float temp, test;*/

        /*initIR();*/
        /*temp = readTemp();*/

        /*printf("temp: %f \n", temp);*/
        /*int width = 50;*/
        /*int height = 50;*/
        /*float * in = (float *)malloc(sizeof(float) * width * height);*/


        /*printf("Start timer!\n");*/
        /*for(int i=0; i<width*height; i++){*/
            /*float temp = readTemp();*/
            /*float color = 255 * 1 / (1 + K*exp(-(temp-CENTER) * A));*/
            /*in[i] = color;*/
            /*sleepS2(WAIT_MS);*/
            /*if (i % width == 0){*/
                /*printf("%d\n", i/width);*/
                /*fflush(stdout);*/
            /*}*/
        /*}*/
        /*printf("End timer!\n");*/

        /*writeBMP(in, width, height);*/
        /*writeConfig();*/
        /*readConfig();*/
}

float readTemp(){
    // adapted from  http://www.raspberrypi.org/phpBB3/viewtopic.php?t=17738&p=362569
    unsigned char i,reg;
    reg = 0x07; // it reads from RAM 0x07
    unsigned char buf[6];
    double temp=0;

    bcm2835_i2c_begin();
    bcm2835_i2c_write(&reg, 1);
    bcm2835_i2c_read_register_rs(&reg, &buf[0], 3);

    temp = (double) (((buf[1]) << 8) + buf[0]);
    temp = (temp * 0.02)-0.00;
    temp = temp - 273.15;
    return (float)temp;
}
void waitMillis(int millis){
    // millis can not be greater than 1000
    usleep(1000 * millis);
}
void initIR(){
    bcm2835_init();
    bcm2835_i2c_begin();
    bcm2835_i2c_set_baudrate((int)BAUD_RATE);
    bcm2835_i2c_setSlaveAddress(ADDRESS);
}

int readConfig(){
    // adapted from  http://www.raspberrypi.org/phpBB3/viewtopic.php?t=17738&p=362569
    unsigned char reg = 0x25; // the command to send
    unsigned char buf[6] = {0,0,0,0,0,0};
    int data=-1;

    bcm2835_i2c_begin();
    int w = bcm2835_i2c_write(&reg, 1);
    int r = bcm2835_i2c_read_register_rs(&reg, &buf[0], 3);
    printf("in read: %d, %d\n", w, r);
    /*bcm2835_i2c_end();*/

    data = buf[0] + (buf[1]<<8);
    return data;
}

void writeConfig(){
    // see http://depa.usst.edu.cn/chenjq/www2/SDesign/JavaScript/CRCcalculation.htm
    // for pec calculation
    unsigned char * write = (unsigned char *)malloc(sizeof(unsigned char) * 4); 
    unsigned char * clear = (unsigned char *)malloc(sizeof(unsigned char) * 4);

    // command, LSB, MSB, PEC
    write[0] = COMMAND; write[1] = LSB; write[2] = MSB; write[3] = PEC;
    clear[0] = COMMAND; clear[1] = 0x00; clear[2] = 0x00; clear[3] = 0x83;

    int c = -1;
    int w = -1;

    // writing the config register
    c = bcm2835_i2c_write(&clear[0], 4);
    printf("c1 = %d  ", c);
    waitMillis(100);
    c = bcm2835_i2c_write(&write[0], 4);
    printf("c2 = %d", c);
    waitMillis(100);

    printf("\n");

    free(clear);
    free(write);
}

void writeBMP(float * in, int w, int h){
    if (DEBUG_PRINT) printf("In writeBMP\n");
    /*int w = 3;*/
    /*int h = 4;*/
    unsigned char * img = (unsigned char *)malloc(3*w*h);


    char filename[] = "photos/ir_00000.bmp";
    char * mode = "w";
    FILE *ofp = fopen(filename, mode);
    int x, y;

    int rowSize = 4 * ((3*w + 3)/4);
    // how many bytes in the row (used to create padding)
    int fileSize = 54 + h*rowSize;
    // headers (54 bytes) + pixel data
    // if name exists, create new filename
    if (!SAME_IMAGE_FILE){
        for (int i=0; i<10000; i++) {
            filename[11] = (i/1000)%10 + '0';    // thousands place
            filename[12] = (i/100)%10 + '0';     // hundreds
            filename[13] = (i/10)%10 + '0';      // tens
            filename[14] = i%10 + '0';           // ones
            if ((ofp = fopen(filename, "r")) == NULL){
                if (DEBUG_PRINT) printf("printing to %s\n", filename);
                break;
            }
        }
    }
    ofp = fopen(filename, mode);

    for (x=0; x<w; x++){
        for (y=0; y<h; y++){
            int R, G, B;
            int val = (unsigned char)in[(y*w + x)];
            if(in[(y*w + x)] < 85){
                R = 0; G = 3*val; B = 255;
            } else if (in[(y*w + x)] < 170){
                R = 3 * (val - 85); G = 255; B = 255 - 3*(val - 85);
            } else if (in[(y*x + x)] < 255){
                R = 255; G = 255 - 3*(val - 170); B = 0;
            }
            if (0) printf("i: %f, R: %d, G: %d, B: %d\n", in[y*w+x], R, G, B);


            img[(y*w + x)*3+0] = B;
            img[(y*w + x)*3+1] = G;
            img[(y*w + x)*3+2] = R;
        }
    }
    if (DEBUG_PRINT) printf("After the for-loop\n");

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

    /*fwrite("%.s", 3, "abcdef"); // example*/
    // want dataFile.write(bmpFileHeader, sizeof(bmpFileHeader));
    //  fwrite(&colorVal, sizeof(unsigned char), 1, ofp);
    fwrite(&bmpFileHeader, sizeof(unsigned char), 14, ofp);
    fwrite(&bmpInfoHeader, sizeof(unsigned char), 40, ofp);

    for (int i=0; i<h; i++){
        //  dataFile.write(img+(w*(h-i-1)*3), 3*w);
        //  dataFile.write(bmpPad, (4-(w*3)%4)%4);  
        fwrite(img+(w*(h-i-1)*3), sizeof(unsigned char), 3*w, ofp);
        /*fwrite(img + 3*w*i, sizeof(unsigned char), 3*w, ofp);*/
        fwrite(&bmpPad, sizeof(unsigned char), (4-(3*w)%4)%4, ofp);
    }




    fflush(ofp);
    
    fclose(ofp);
}

void writePPM(){
    int width = 100;
    int height = 100;
    if (DEBUG_PRINT) printf("In writePPM...");



    long long int i;
    /*char filename[] = "ir_00000.ppm";*/
    // malloc, since we want to return the address (and not a local)
    char * filename = (char *)malloc(sizeof(char)*(8+1+3));
    filename = "ir_00000.ppm";
    char mode[] = "w";
    // auto increment name if file already exists

    // if name exists, create new filename
    /*for (int i=0; i<10000; i++) {*/
        /*filename[4] = (i/1000)%10 + '0';    // thousands place*/
        /*filename[5] = (i/100)%10 + '0';     // hundreds*/
        /*filename[6] = (i/10)%10 + '0';      // tens*/
        /*filename[7] = i%10 + '0';           // ones*/
        /*[>if (!SD.exists(filename)){<]*/
            /*break;*/
        /*[>}<]*/
    /*}*/

    FILE * ofp = fopen(filename, mode);


    fprintf(ofp, "P6");
    fprintf(ofp, "\n");
    fprintf(ofp, "%d ", width);
    fprintf(ofp, "%d ", height);
    fprintf(ofp, " %d ", 255);
    fflush(ofp);

    int32_t length = 1;
    length = length * width;
    length = length * height;
             

    for (i=0; i<length; i++){
        unsigned char colorVal =  115;
        fwrite(&colorVal, sizeof(unsigned char), 1, ofp);
        fwrite(&colorVal, sizeof(unsigned char), 1, ofp);
        fwrite(&colorVal, sizeof(unsigned char), 1, ofp);
    }
    fflush(ofp);
    fclose(ofp);
}
