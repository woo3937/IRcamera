/* This code fails currently on the Arduino Uno. The Uno only has 2k of RAM
 * -2013-06-07 
 */
/* TO WRITE TO THE SD CARD:
 *         - first, connect the SD card shield so ALL the pins connect
 *         - #include <SD.h>, const int chipSelect = 4
 *         - FILE dataFile = SD.open("datalog.txt", FILE_WRITE)
 *         - if(dataFile){
 *                      dataFile.println(dataString);
 *                      dataFile.close()
 *
 *  
 */
/*
    SD card datalogger
 
 This example shows how to log data from three analog sensors 
 to an SD card using the SD library.
 	
 The circuit:
 * analog sensors on analog ins 0, 1, and 2
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4
 
 created    24 Nov 2010
 modified 9 Apr 2012
 by Tom Igoe
 
 This example code is in the public domain.
 	 
 */

#include <SD.h>
#include <i2cmaster.h>
//#include <SPI.h>
//#include <Wire.h>
//#include <EEPROM.h>
//#include <I2C.h>
//#include <SDFat.h>
//#include <SDFatUtil.h>

const int chipSelect = 8;
// must change from 4 to 8! (8 on sparkfun shield)

//SdFat sd;
//SdFile file;
const uint8_t cardPin = 8;                    
// pin that the SD is connected to (8 for SparkFun MicroSD shield, 4 for others )




void setup(){
    // setting up the serial port
    Serial.begin(9600);
    while(!Serial);

    // setting up the output pins
    pinMode(10, OUTPUT); pinMode(9, OUTPUT);
    if (!SD.begin(chipSelect)){
        Serial.println("It did the SD-if statement");
        return;
    }
    Serial.println("Done with serial port setup...\n");

    // setting up the IR
    setupIR();
    
    // width, height < 10 (only 2k memory on the Uno)
    int width = 15;
    int height = 10;
    
    float * x = takePicture(width, height);
    int   *xx = (int *)malloc(sizeof(int)*width*height);
    
    for (int i=0; i<width*height; i++){
        xx[i] = (int)(x[i]*5);
    }

    // fail because the Arduino Uno only has 2k of RAM
    //writeBMPImage(xx,"debug.bmp" ,width, height);
//    writePPMImage(xx, width, height, "debug.ppm");
}

void loop(){
  float temp = 0;
  temp = readTemp();
  Serial.print(temp); Serial.println(" degrees Celcius");
  delay(1000);
}

float * takePicture(long int width, long int height){
    // assumes width, height of 11, 11
    // 
    int xx, yy;
    
    int HORIZPIN = 9;
    int VERTPIN = 10;
    float * x = (float *)malloc(sizeof(float) * width * height);

    for (xx=0; xx<width; xx++){
        Serial.print(width);Serial.print("   xx == ");Serial.println(xx);
        for (yy=0; yy<height; yy++){
            Serial.print("    "); Serial.println(j);
            gotoPixel(xx, yy, HORIZPIN, VERTPIN, width, height);
            x[i*width + j] = 0;
            
            x[yy*width + xx] = 115;//readTemp();
//            delay(10);
//            Serial.print("in takePicture(): readTemp== ");
//            Serial.println(x[yy*width + xx]);
//            delay(10);
        }      
    }
    
    return x;
  
}

void setupIR(){
    i2c_init();
    
    // enabling pullups
    PORTC = (1 << PORTC4) | (1 << PORTC5); 
}

void writePPMImage(int * data, int w, int h, char filename[]){
    // assumes that 0 < data[i] < 255
  
    // the file where we're going to write to
    File dataFile;
    char name[] = "test.ppm";
    int height = h;
    int width = w;
    // we can't open a file that already exists...
    if(SD.exists(name)) SD.remove(name);
    dataFile = SD.open(name, FILE_WRITE);
    
    // P3 means RGB color in the PPM format
    dataFile.println("P3");
    
    // width and height
    dataFile.print(w); dataFile.print(" ");
    dataFile.println(h);
    
    // setting the max color
    dataFile.println(255);
    
    int xx, yy;
    for (yy=0; yy<height; yy++){
        for (xx=0; xx<width; xx++){
            int R, G, B, C;
            C = data[yy*width + xx];
            Serial.print(C);
            Serial.write(C);
            Serial.println("   ");
            R = C;
            G = C;
            B = C; // change R,G,B to a red-blue colormap later
            dataFile.print(R); // R
            dataFile.print(" "); 
            
            dataFile.print(G); // G
            dataFile.print(" ");
            
            dataFile.print(B); // B
            dataFile.print(" ");
        }
        dataFile.print("\n");
    }
    dataFile.close();
  
}




float readTemp(){
    // for this specific IR sensor. change if using a different one.
    int dev = 0x5A << 1;
    int data_low;
    int data_high;
    int pec;
    
    // from the comment by Sensorjunkie at http://forum.arduino.cc/index.php/topic,21317.0.html
    i2c_start_wait(dev + I2C_WRITE);
    i2c_write(0x07);
    i2c_rep_start(dev+I2C_READ);
    data_low = i2c_readAck();
    data_high = i2c_readAck();
    pec = i2c_readNak();
    i2c_stop();
    
    double tempFactor = 0.02;
    float temp=0;
    
    // from the datasheet
    int data = (data_high << 8) + data_low;
    temp = data * 0.02 - 273.15;
    return temp;
}


void gotoPixel(int vertical, int horizontal, int vertPin, int horizPin, int height, int width){
    // hard coded: the width of the image.
    // right now, it assumes we want a picture (100/255) * 170 degrees wide
    // 100 is the value that's hard coded in
    
    int vertPWM = vertical  * 100 / height;
    int horizPWM = horizontal * 100 / width;
    analogWrite(horizPin, horizPWM);
    analogWrite(vertPin, vertPWM);
    //delay(80);
    // delay 40ms
        
    return;
}



void writeBMPImage(int * input, char fileName[], int w, int h){
    // Works, but only for small (about 10x10) images. I'm saying "screw it" and
    // encoding the image in the PPM format -- see writePPMImage instead.
    
    //Serial.write("width == "); Serial.println(w);
    //Serial.write("height == "); Serial.println(h);
    // SD setup
    // as of now, this function does NOT write to the filename. Instead, it writes to 
    // "toDebug.bmp"
    
    //Serial.begin(9600);
    //if (!sd.init(SPI_FULL_SPEED, cardPin)) {
    //    sd.initErrorHalt();
    //    Serial.println("---");
    //}
    char name[] = "bur.bmp";
    Serial.print("In the writeBMPImage, writing ");
    Serial.write(name);
    Serial.write("\n\n");
   
    

    // DEBUG: make it so you can pass a name in...
    
    File dataFile;
    // we can't open a file that already exists...
    if(SD.exists(name)) SD.remove(name);
    dataFile = SD.open(name, FILE_WRITE);
    //while(!dataFile);
    Serial.write("dataFile == ");Serial.println(dataFile);
    // set fileSize (used in bmp header)
    int rowSize = 4 * ((3*w + 3)/4);            // how many bytes in the row (used to create padding)
    int fileSize = 54 + h*rowSize;                // headers (54 bytes) + pixel data
    Serial.write("fileSize == "); Serial.println(fileSize);
    Serial.write("rowSize == "); Serial.println(rowSize);
    // create image data; heavily modified version via:
    // http://stackoverflow.com/a/2654860
    unsigned char *img = NULL;                        // image data
    if (img) {                                                        
      // if there's already data in the array, clear it
        free(img);
    }
    img = (unsigned char *)malloc(3*w*h);

    for (int y=0; y<h; y++) {
        for (int x=0; x<w; x++) {
            int colorVal = input[y*w + x];            // classic formula for px listed in line
            //Serial.println(colorVal);
            img[(y*w + x)*3+0] = (unsigned char)(colorVal);        // R
            img[(y*w + x)*3+1] = (unsigned char)((colorVal));        // G
            img[(y*w + x)*3+2] = (unsigned char)(colorVal);        // B
            // padding (the 4th byte) will be added later as needed...
        }
    }

    // print px and img data for debugging
    if (0) {
        Serial.print("\nWriting \"");
        Serial.print("\"");Serial.print(name); Serial.print("\" ");
        Serial.print("\" to file...\n");
        for (int i=0; i<w*h; i++) {
            Serial.print(input[i]);
            Serial.print("    ");
        }
    }

    // create padding (based on the number of pixels in a row
    //unsigned char bmpPad[rowSize - 3*w];
    unsigned char * bmpPad = (unsigned char *)malloc(sizeof(unsigned char) * (rowSize - 3*w));
    for (int i=0; i<rowSize-3*w; i++) {                 
        // fill with 0s
        bmpPad[i] = 0;
    }

    // create file headers (also taken from StackOverflow example)
    unsigned char bmpFileHeader[14] = {                        // file header (always starts with BM!)
        'B','M', 0,0,0,0, 0,0, 0,0, 54,0,0,0     };
    unsigned char bmpInfoHeader[40] = {                        // info about the file (size, etc)
        40,0,0,0, 0,0,0,0, 0,0,0,0, 1,0, 24,0     };

    bmpFileHeader[ 2] = (unsigned char)(fileSize            );
    bmpFileHeader[ 3] = (unsigned char)(fileSize >>    8);
    bmpFileHeader[ 4] = (unsigned char)(fileSize >> 16);
    bmpFileHeader[ 5] = (unsigned char)(fileSize >> 24);

    bmpInfoHeader[ 4] = (unsigned char)(             w            );
    bmpInfoHeader[ 5] = (unsigned char)(             w >>    8);
    bmpInfoHeader[ 6] = (unsigned char)(             w >> 16);
    bmpInfoHeader[ 7] = (unsigned char)(             w >> 24);
    bmpInfoHeader[ 8] = (unsigned char)(             h            );
    bmpInfoHeader[ 9] = (unsigned char)(             h >>    8);
    bmpInfoHeader[10] = (unsigned char)(             h >> 16);
    bmpInfoHeader[11] = (unsigned char)(             h >> 24);
    
    //Serial.write(bmpFileHeader, sizeof(bmpFileHeader));
    //Serial.println(*bmpInfoHeader);
    // write the file (thanks forum!)
    dataFile.write(bmpFileHeader, sizeof(bmpFileHeader));
    delay(100);
    dataFile.write(bmpInfoHeader, sizeof(bmpInfoHeader));
    delay(100);
    //file.write(bmpFileHeader, sizeof(bmpFileHeader));        // write file header
    //file.write(bmpInfoHeader, sizeof(bmpInfoHeader));        // " info header

    for (int i=0; i<h; i++) {                                                        // iterate image array
        dataFile.write(img+(w*(h-i-1)*3), 3*w);
        delay(200);
        //file.write(img+(w*(h-i-1)*3), 3*w);                                // write px data
        dataFile.write(bmpPad, (4-(w*3)%4)%4);                                 // and padding as needed
        delay(200);
    }
    dataFile.close();                                                                                // close file when done writing

    if (0) {
        Serial.print("\n\n---\n");
    }
}



void writePlainTextImage(int * pix, int w, int h){
    int x; 
    int y;
    
    File file = SD.open("wxn.txt");
    
    for(y=0; y<h; y++){
      for (x=0; x<w; x++){
        file.print(x); file.write(",");
      }
    }
    file.close();
    
  
}

int freeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

