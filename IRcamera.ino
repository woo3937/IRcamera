/* This code fails currently on the Arduino Uno. The Uno only has 2k of RAM
 * -2013-06-07 
 * 
 * Then, we must use the SD card (~2GB) as our RAM. Slow, but nothing compared to
 * servos.
 * -2013-06-10
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
#include <Servo.h>
//#include <SPI.h>
//#include <Wire.h>
//#include <EEPROM.h>
//#include <I2C.h>
//#include <SDFat.h>
//#include <SDFatUtil.h>

const int chipSelect = 8;
// must change from 4 to 8! (8 on sparkfun shield)
Servo horizServo;
Servo vertServo;
//SdFat sd;
//SdFile file;
const uint8_t cardPin = 8;                    
// pin that the SD is connected to (8 for SparkFun MicroSD shield, 4 for others )

// TODO: write readPixel()
// seek is my friend
// seek to a new position
// print all 0's

unsigned char readPixel(long int i, char * filename){
    File dataFile = SD.open(filename);
    dataFile.seek(11 + 3*i);
    
    unsigned char R = dataFile.read(); // R
    unsigned char G = dataFile.read(); // G
    unsigned char B = dataFile.read(); // B
    
    if(B == 255){
        return G/3;
    } else if (G == 255){
        return 255 - B/3;
    } else if (R == 255){
        return 255 - G/3;
    }
    
    // TODO: look at the gradient we want, and does G play a role?
    // return G, since that it unused (?) in the scheme we want
    return -1;
    // for error...
  
}
void writePixel2(long int i, File dataFile, unsigned char x){
    // assumes file.open() has been called earlier
    // assumes file.close() will be called later
        unsigned char R, G, B;  
    if(x <= 85){
        R = 0;
        G = 3*x;
        B = 255;
      
    } else if (x <= 170){
        R = 3 * (x - 85);
        G = 255;
        B = 255 - 3*(x - 85);
      
    } else if (x <= 255){
        R = 255;
        G = 255 - 3*(x - 170);
        B = 0;
    } else Serial.println("writePixel: error!");
    
    boolean as = dataFile.seek(11 + 3*i + 4);
    dataFile.write(R);
    dataFile.write(G);
    dataFile.write(B);
}

void writePixel(long int i, char * filename, unsigned char x){
    // takes in an index, like arrays (0 based)
    File dataFile;
    dataFile = SD.open(filename, FILE_WRITE);
//    Serial.print("dataFile == ");
//    Serial.println(dataFile);
//    Serial.println(filename);

    

    unsigned char R, G, B;  
    if(x <= 85){
        R = 0;
        G = 3*x;
        B = 255;
      
    } else if (x <= 170){
        R = 3 * (x - 85);
        G = 255;
        B = 255 - 3*(x - 85);
      
    } else if (x <= 255){
        R = 255;
        G = 255 - 3*(x - 170);
        B = 0;
    } else Serial.println("writePixel: error!");
    
    boolean as = dataFile.seek(11 + 3*i + 4);
    dataFile.write(R);
    dataFile.write(G);
    dataFile.write(B);
    dataFile.close();
}

void setup(){
    // setting up the serial port
    Serial.begin(9600);
    while(!Serial);
    
    Serial.println("Start...");
    

    // setting up the output pins
    pinMode(10, OUTPUT); pinMode(9, OUTPUT);
    
    // if the SD card isn't there, return
    if (!SD.begin(chipSelect)){
        Serial.println("SD?");
        return;
    }

    // setting up the IR
    setupIR();
    
    
//    horizServo.attach(9);
//    vertServo.attach(10);
    
    //unsigned char * x = takePicture(width, height);
    
    // returns a filename, so we can pass it to other functions
    // a filename of a total of 12 characters long (8.3 format)
//    int time = millis();
//    char * name = initPPM(width, height);
//    time = millis() - time;
//    Serial.print("Time in initPPM:\n");Serial.println(time/1000.0);
//    Serial.print("filename == "); Serial.println(name);
//
//    //writePixel(2, name, 255);
//    File dataFile;
//    dataFile = SD.open(name, FILE_WRITE);
//
//    for (int i=0; i<width*height; i++){
////        time = micros();
//        float colorVal = 255.0*i / (100.0*100.0);
//        writePixel2(i, dataFile, (int)colorVal);
////        time = micros() - time;
////        Serial.println(time);
//        if (i%100 == 0) Serial.println(i/width);
//    }
//    dataFile.close();

    // width, height < 10 (only 2k memory on the Uno)
    int width = 100;
    int height = 100;
    

    
    // printing the free RAM
    Serial.print("\n\nFree RAM:\n");
    Serial.println(freeRam());
    Serial.println("-----");
    pinMode(9, OUTPUT);
    
    horizServo.attach(10);
    vertServo.attach(9);
    horizServo.write(0);
    vertServo.write(0);
    takePicture(width, height);
}

void loop(){
  float temp = 0;
//  temp = readTemp();
  int HORIZPIN = 9;
  int VERTPIN = 10;
  int width = 100;
  int height = 100;

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


void gotoPixel(int x, int y, Servo horizServo, Servo vertServo, int height, int width){
    // assumes horizServo and vertServo have called .attach(pin) before
    // assumes angle of 45 degrees
    int angle = 45;
    unsigned char horizAngle = 1.0 * x * angle / width;
    unsigned char vertAngle = 1.0 * y * angle / height;
    
    float horizLastAngle = horizServo.read();
    float vertLastAngle = vertServo.read();
    
    horizServo.write(horizAngle);
    vertServo.write(vertAngle);
    
    // delay = 0.14 sec / 60 degrees
    float delay2 = 1000 * 1000 * (horizAngle - horizLastAngle)  * 0.14 / 60;
    if (delay2 < 0) delay2 = -1 * delay2;
    
    delayMicroseconds((int)delay2*1000);
  
}

unsigned char * takePicture(int width, int height){
    // assumes width, height of 11, 11
    // 
    int xx, yy;
    
    int HORIZPIN = 9;
    int VERTPIN = 10;
    char * name = initPPM(width, height);
    File file = SD.open(name, FILE_WRITE);
    Serial.print("in takePicture, printing \n");
    Serial.println(name);
    Serial.println();

    for (yy=0; yy<width; yy++){
        Serial.print(width);Serial.print("   \t\tyy == ");Serial.println(yy);
        for (xx=0; xx<height; xx++){
              int horizPixel;
              if (yy%2 == 0)  horizPixel = xx;
              if (yy%2 == 1)  horizPixel = width - xx - 1;
              gotoPixel(horizPixel, yy, horizServo, vertServo, width, height);
              delay(80);
//              Serial.println(horizPixel);

              

            // returns a floating point value
            float temp = readTemp();
            Serial.print(temp);

            
            // we're taking temperature values between -20 and 108
            float a = 3.8e-1;
            float e = 2.718281828459045;
            temp = 255 * 1 / (1 + pow(e, -(temp-30) * a));
            
            //temp = 1 / (1 + e**(-(temp-35) * a))
            //temp += b * temp * temp;
            //temp += 15;
            Serial.print("\t");
            Serial.print(temp);
            Serial.print("\n");
            writePixel2(horizPixel + yy*width, file, (unsigned char)temp);
        }
        //delay(1000);      
    }
    file.close();
    delay(100);
    Serial.println("Done");
    
//    return 0;
  
}

void setupIR(){
    i2c_init();
    
    // enabling pullups
    PORTC = (1 << PORTC4) | (1 << PORTC5); 
}





char * initPPM(int width, int height){
    Serial.println("\nIn initPPM");
    long long int i;
    //char filename[] = "ir_00000.ppm";
    // malloc, since we want to return the address (and not a local)
    char * filename = (char *)malloc(sizeof(char)*(8+1+3));
    filename = "ir_00000.ppm";
    // auto increment name if file already exists

      // if name exists, create new filename
  for (int i=0; i<10000; i++) {
    filename[4] = (i/1000)%10 + '0';    // thousands place
    filename[5] = (i/100)%10 + '0';     // hundreds
    filename[6] = (i/10)%10 + '0';      // tens
    filename[7] = i%10 + '0';           // ones
    if (!SD.exists(filename)) {
      Serial.println("Did the if");
      break;
    }
  }
    
    // opening the file, deleting if there's already one
    File dataFile;
    if(SD.exists(filename)) SD.remove(filename);
    dataFile = SD.open(filename, FILE_WRITE);
    
    dataFile.print("P6");
    // specifing a PPM binary RGB file

    //dataFile.write("\n");
    dataFile.print(" ");
    dataFile.print(width);
    dataFile.print(" ");
    dataFile.print(height);
    dataFile.print(" ");
    //dataFile.print(0xFF);
    dataFile.print(255);
    dataFile.write(0x0A);

    Serial.println("\nPosition()");
    Serial.println(dataFile.position());
    Serial.println("end position()\n");
    int32_t length = 1; 
    // since we're printing R, G, and B values in one loop
    length = length * width;
    length = length * width;
    Serial.println(length);
   
    
    for (i=0; i<length; i++){
        //Serial.write(i);
        unsigned char colorVal = 115;
        dataFile.write(colorVal);
        dataFile.write(colorVal);
        dataFile.write(colorVal); 
    }
    dataFile.close();
    
    // return the filename written?
    return filename;
}


// -----------------------------------------------------------------------------
// ------------------- below or "writeImage" functions of various complexity ---   
// -----------------------------------------------------------------------------

void writePPMImage(unsigned char * data, int w, int h, char filename[]){
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

void writeBMPImage(unsigned char * input, char fileName[], int w, int h){
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
        //file.write(img+(w*(h-i-1)*3), 3*w);                                
        // write px data
        dataFile.write(bmpPad, (4-(w*3)%4)%4);                                 
        // and padding as needed
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

