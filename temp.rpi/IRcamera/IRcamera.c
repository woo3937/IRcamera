/*
 * We need to...
 *  (- is kinda, x done, o is open)
 *      - move the sensor where ever we want to
 *      x write an image out
 *      x implement the haar transform
 *      - implement a basic algorithm (FISTA)
 *      o implement the complex waveform
 *
 *      -- Scott Sievert, 2013-7-22, sieve121 (at) umn (dot) edu
 */
/*
 * IMPORTANT HARDWARE NOTE:
 *  As of 2013-07-30, horizStepper refers to the stepper that rotates in the
 *  vertical direction, but who's motor is horizontal (flipped for the
 *  vertStepper). This depends on the USB drives and the acceleration/velocity limits.
 */
    /*
     *  My wires are hooked up to the following GPIO pins:
     *  
     * | Pin | GPIO pin |
     * | SDA | 2        |
     * | SCL | 3        |
     * | PWR | 4        |
     * | GND | 17       |
     *
     * On the MLX6014xxx, Vss(GND), Vdd(PWR), SDA and SCL are here:
     *      (note that the || means the pin on the device)
     *           .__.        
     *           |  |                          
     *    .______|  |_______.                    
     *    |                 |          
     *    |  Vss      SCL   |          
     *    |                 |           
     *    |                 |           
     *    |  Vdd      SDA   |           
     *    |                 |           
     *    |_________________|           
     *
     *    --Scott Sievert, 2013-07-19, sieve121 (at) umn (dot) edu
     */
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
     *  --Scott Sievert (sieve121 (at) umn (dot) edu), 2013-06-26
     */

#include <stdio.h>
#include <string.h>
#include <bcm2835.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>
#include <phidget21.h>
#include "steppers.h"
#include "brain.h"
#include "IRcamera.h"
#include <unistd.h>

/*#define WIDTH 100*/
/*#define HEIGHT 100*/

#define PWR_PIN 4

#define BAUD_RATE 100e3
#define DEBUG_PRINT 1

/*#define WAIT_MS 40 // note that the motors (as of 2013-06-27) wait until they're in position*/
/*#define SAME_IMAGE_FILE 1*/
/*#define MIN_TEMP 10*/
/*#define MAX_TEMP 60*/

#define ADDRESS 0x00
#define COMMAND 0x25
#define MSB 0xb1
#define LSB 0x74
#define PEC 0x6b

void initIR();
float readTemp();
int readConfig();
void writeConfig();
void waitMillis(int millis);
void writeConfigParams( unsigned char command, unsigned char lsb,
                        unsigned char msb,     unsigned char pec);
void writeImage(char filename[50], float * data, int width, int height);
unsigned char findPec(unsigned char comm, unsigned char lsb, unsigned char msb);
void testSpeed(CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper,
        int width, int height);
void setMotorToInitialState(CPhidgetStepperHandle stepper, __int64 loc);
void testIRSensor();


int main(int argc, char **argv){
    /*testFunctions();*/

    int data;
    float temp, temp1;
    int repeat=0;
    unsigned char pec;
    unsigned char comm = 0x25;
    unsigned char lsb = 0x74;
    unsigned char msb = 0xb1;
    initIR();
    writeConfigParams(comm, lsb, msb, pec);
    waitMillis(400);
    data = readConfig();
    printf("CONFIG: %x\n", data);
    printf("WAIT_MS: %d\n", WAIT_MS);
    temp = readTemp();
    printf("SAMPLE_TEMP: %f\n", temp);
    printf("\n\n");

    // init'ing the image
    int xx, yy, i, j;

    // init'ing our steppers
    int stepH = 0;
    int indH  = 322212;
    indH = -1;
    CPhidgetStepperHandle horizStepper = stepH;
    CPhidgetStepper_create(&horizStepper);
    initStepper(horizStepper, stepH, indH);

    int stepV = 0;
    int indV = -1;
    CPhidgetStepperHandle vertStepper = stepV;
    CPhidgetStepper_create(&vertStepper);
    initStepper(vertStepper, stepV, indV);

    float loc = ANGLE/2;
    // what location gives that angle?
    loc = loc * (1200 * 16) / 360.0f;   // deg * steps/deg

    // setting the current position, and checking
    CPhidgetStepper_setCurrentPosition(horizStepper, 0, (__int64)loc);
    CPhidgetStepper_setCurrentPosition(vertStepper, 0, (__int64)loc);

    // setting vertStepper to be slower -- more mass/load.
    // vertStepper can max out then.
    setVelocity(horizStepper, 1e-1);
    setVelocity(vertStepper, 5e-2);
    setAcceleration(vertStepper, 5e-2);
    setAcceleration(horizStepper, 1e-1);

    /*goDeltaAngle(vertStepper, -180);*/

    int N = 128;
    int width  = N;
    int height = N;

    float * xold = (float *)malloc(sizeof(float) * width *height);
    for (i=0; i<N*N; i++) xold[i] = 0;
    int wait_ms = 40;
    // getting the wait times right
    wait_ms = (46 * wait_ms) / 51;
    printf("wait_ms: %d\n", wait_ms);
    /*testIRSensor();*/
    /*getMeasurementsFromBranch(horizStepper, vertStepper, xold, wait_ms,*/
            /*0, width/1, 0, height/1, 1, width, height);*/
    /*getMeasurementsFromBranch(horizStepper, vertStepper, xold, 46,*/
            /*0*width/1, width/1, 0*height/1, height/1, 1, width, height);*/
    /*writeImage("full.png", xold, width, height);*/
    mainIST(width, height, horizStepper, vertStepper);

    setMotorToInitialState(horizStepper, (__int64)loc);
    setMotorToInitialState(vertStepper, (__int64)loc);

    /*goDeltaAngle(horizStepper, -15);*/
    /*goDeltaAngle(vertStepper, -20);*/
    // setting it back to the middle
    delay(5000);
    // ending I2C operations
    bcm2835_i2c_end();
}
void testIRSensor(){
    float temp;
    temp = readTemp();
    printf("tempTest: %f\n", temp);

}
void setMotorToInitialState(CPhidgetStepperHandle stepper, __int64 loc){
    setVelocity(stepper, 1e-2);
    setAcceleration(stepper, 5e-1);
    CPhidgetStepper_setTargetPosition(stepper, 0, loc);
}

void testSpeed(CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper,
        int width, int height){
    int horizPixel;
    for (int yy=0; yy<height; yy++){
        if (yy%2 == 0) horizPixel = width-1;
        if (yy%2 == 1) horizPixel = 0;
        gotoPixel2D(horizStepper, 0, vertStepper, 0, horizPixel, width, yy, height);
    }
    gotoPixel2D(horizStepper, 0, vertStepper, 0, width/2, width, height/2, height);

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
    /*usleep(1000 * millis);*/
    delay(millis);
}
void initIR(){
    bcm2835_init();
    bcm2835_i2c_begin();
    bcm2835_i2c_set_baudrate((int)BAUD_RATE);
    bcm2835_i2c_setSlaveAddress(ADDRESS);

    // setting up the PWR pin and turning it on
    bcm2835_gpio_fsel( PWR_PIN, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_write(PWR_PIN, HIGH);
    waitMillis(999);
}
int readConfig(){
    // adapted from  http://www.raspberrypi.org/phpBB3/viewtopic.php?t=17738&p=362569
    unsigned char reg = 0x25; // the command to send
    unsigned char buf[6] = {0,0,0,0,0,0};
    int data=-1;

    bcm2835_i2c_begin();
    int w = bcm2835_i2c_write(&reg, 1);
    int r = bcm2835_i2c_read_register_rs(&reg, &buf[0], 3);

    data = buf[0] + (buf[1]<<8);
    return data;
}
void writeConfigParams( unsigned char command, unsigned char lsb,
                        unsigned char msb,     unsigned char pec){
    // see http://depa.usst.edu.cn/chenjq/www2/SDesign/JavaScript/CRCcalculation.htm
    // for pec calculation
    unsigned char * write = (unsigned char *)malloc(sizeof(unsigned char) * 4); 
    unsigned char * clear = (unsigned char *)malloc(sizeof(unsigned char) * 4);

    // command, LSB, MSB, PEC
    pec = findPec(command, lsb, msb);
    /*printf("%x: pec", pec);*/
    write[0] = command; write[1] = lsb; write[2] = msb; write[3] = pec;
    clear[0] = command; clear[1] = 0x00; clear[2] = 0x00; clear[3] = 0x83;
    // assumes command = 0x25 (for PEC value)

    int c = -1;
    int w = -1;

    // first, clear and wait for EEPROM to settle
    c = bcm2835_i2c_write(&clear[0], 4);
    waitMillis(100);

    // then write, waiting for EEPROM to settle
    c = bcm2835_i2c_write(&write[0], 4);
    waitMillis(100);

    // requires bcm2835_gpio_fsel(4, BCM2835_GPIO_FSEL_OUTP); to be called.
    // turn it off, and wait for it to turn off
    bcm2835_gpio_write(PWR_PIN, LOW);
    waitMillis(100);

    // turn it on, and wait for it to turn on all the way
    bcm2835_gpio_write(PWR_PIN, HIGH);
    waitMillis(100);

    free(clear);
    free(write);
}

unsigned char findPec(unsigned char comm, unsigned char lsb, unsigned char msb){
    if(comm==0x25){
        if(lsb==0x74){
            if(msb==0xb7) return 0x79;
            if(msb==0xb6) return 0x7e;
            if(msb==0xb5) return 0x77;
            if(msb==0xb4) return 0x70;
            if(msb==0xb3) return 0x65;
            if(msb==0xb2) return 0x62;
            if(msb==0xb1) return 0x6b;
        }
        if (lsb==0x75){
            if(msb==0xb1) return 0x7e;
            if(msb==0xb2) return 0x77;
            if(msb==0xb3) return 0x70;
            if(msb==0xb4) return 0x65;
            if(msb==0xb5) return 0x62;
            if(msb==0xb6) return 0x6b;
            if(msb==0xb7) return 0x6c;
        }
    }
    printf("The combination for the PEC wasn't found!\n\n\n");
    return -1;

}

// writeImageWithFilename writes a csv file than has python write the image
// the filename must be less that 40 characters (shouldn't be a problem)
void writeImage(char filename[40], float * data, int width, int height){
    // delete the file, open the file, write the data to *.csv
    // process the data with the python script writeImage.py
    system("rm image.csv");
    FILE * file = fopen("image.csv", "w");
    int x=0;
    int y=0;

    // print to a file (a csv)
    for (y=0; y<height; y++){
        for (x=0; x<width; x++){
            /*if(1 && y*width + x < 10) printf("%.2f\n", data[y*width + x]);*/
            fprintf(file, "%.2f", data[y*width + x]);
            if(x<width-1) fprintf(file, ",");
        }
        fprintf(file, "\n");
    }
    fclose(file);
    
    char command[50] = "python writeImage.py ";
    strcat(command, filename);
    printf("%s\n", command);
    system(command);
    /*system("rm image.csv");*/
}
