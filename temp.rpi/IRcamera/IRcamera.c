#include <stdio.h>
#include <bcm2835.h>
/*#include <wiringPi.h>*/
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>

#define BAUD_RATE 50e3
#define DEBUG_PRINT 1


#define WAIT_MS 24.0f
#define SAME_IMAGE_FILE 1

// the constants that determines the width of blue-red
#define A 2.4e-1f
#define CENTER 30.0f
#define K 1.0f // since B taken in RGB
#define E 2.718281828459045f

void initIR();
float readTemp();
void writeBMP(float * in, int w, int h);
void writePPM();
void sleepS2(float mills);
float readConfig();
void writeConfig();

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

void main(int argc, char **argv){
    float temp, test;

    initIR();
    temp = readTemp();

    printf("temp: %f \n", temp);
    int width = 50;
    int height = 50;
    float * in = (float *)malloc(sizeof(float) * width * height);

    printf("Start timer!\n");
    for(int i=0; i<width*height; i++){
        float temp = readTemp();
        float color = 255 * 1 / (1 + K*exp(-(temp-CENTER) * A));
        in[i] = color;
        sleepS2(WAIT_MS);
        if (i % width == 0){
            printf("%d\n", i/width);
            fflush(stdout);
        }
    }
    printf("End timer!\n");

    writeBMP(in, width, height);
    writeConfig();
    readConfig();

        printf("Starting wait...\n");
        for (int i=0; i<1000; i++){
            sleepS2(WAIT_MS);
        }
        printf("Ending wait\n");


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
void initIR(){
    bcm2835_init();
    bcm2835_i2c_begin();
    bcm2835_i2c_set_baudrate((int)BAUD_RATE);
    bcm2835_i2c_setSlaveAddress(0x5a);
}

void sleepS2(float mills){
    // a shitty wait function. might be influenced by some stuff in the linux
    // kernel. accurate within ~3%
    mills = 17.4e3 * mills;
    while (mills > 0) mills = mills-1;

}
float readConfig(){
    // adapted from  http://www.raspberrypi.org/phpBB3/viewtopic.php?t=17738&p=362569
    unsigned char reg = 0x25; // the command to send
    unsigned char buf[6] = {0,0,0,0,0,0};
    int data=-1;

    bcm2835_i2c_begin();
    bcm2835_i2c_write(&reg, 1);
    bcm2835_i2c_read_register_rs(&reg, &buf[0], 3);

    data = buf[0] + (buf[1]<<8);
    if(DEBUG_PRINT) printf("data: 0x%x\n", data);
    return (float)1;
}

void writeConfig(){
    unsigned char com[] = {0x25, 0x74, 0xb1, 0x6b};
    unsigned char clear[] = {0x25, 0x00, 0x00, 0x83};

    bcm2835_i2c_begin();
    bcm2835_i2c_write(&clear[0], 4);
    bcm2835_i2c_begin();
    bcm2835_i2c_write(&com[0], 4);
}

