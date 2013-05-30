/* TO WRITE TO THE SD CARD:
 *         - first, connect the SD card shield so ALL the pins connect
 *         - #include <SD.h>, const int chipSelect = 4
 *         - FILE dataFile = SD.open("datalog.txt", FILE_WRITE)
 *         - if(dataFile){
                        dataFile.println(dataString);
                        dataFile.close()

    

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
//#include <SDFat.h>
//#include <SDFatUtil.h>
const int chipSelect = 8;
// must change from 4 to 8!

//SdFat sd;
//SdFile file;
const uint8_t cardPin = 8;                    // pin that the SD is connected to (d8 for SparkFun MicroSD shield)




void setup(){
    
    Serial.begin(9600);
    while(!Serial);
    //Serial.println("At beginning of setup...\n");
    pinMode(10, OUTPUT); pinMode(9, OUTPUT);
    digitalWrite(10, HIGH);
    if (!SD.begin(chipSelect)){
        Serial.println("It did the SD-if statement");
        return;
    }
    Serial.println("Done with serial port setup...\n");


    char name[] = "9px_0000.bmp";             // filename convention (will auto-increment)
    // iteratively create pixel data
    const int w = 13;                                     // image width in pixels
    const int h = 10; 
    Serial.println("Before the malloc call");
    int * px1 = (int *)malloc(sizeof(int) * w * h);
    Serial.println("After the malloc call\n");
    int increment = 256/(w*h);                // divide color range (0-255) by total # of px

                                       // " height
    const boolean debugPrint = true;        // print details of process over serial?

    const int imgSize = w*h;
    //Serial.println("Before the pix1[w*h] declaration");
    //int px1[w*h];                                                // actual pixel data (grayscale - added programatically below)

    // assumes we have a grey-scale image
    for (int i=0; i<imgSize; i++) {
        px1[i] = i * increment;                    // creates a gradient across pixels for testing
    }
    Serial.println("Beginning write..."); delay(2);
    writeBMPImage(px1,"testinggg.txt", w, h);
    Serial.println("Ending write...");
    
    //writePlainTextImage(px1, 4, 4);

}

void loop(){

  Serial.println("We are in the loop");
  // it's going between 0 and 15 degrees
  // HARDWARE BUG: I'm pretty sure a servo is bad. One always goes, no matter what. Swapping inputs doesn't help.
  delay(1000);
  gotoPixel(40, 40, 9, 10, 100, 100);
  delay(1000);
  gotoPixel(0, 0, 9, 10, 100, 100);
  //analogWrite(9, 15);
  //analogWrite(9, 100);
  delay(100);
  //analogWrite(10, j);
  
    
}

void gotoPixel(int vertical, int horizontal, int vertPin, int horizPin, int height, int width){
    // hard coded: the width of the image.
    // right now, it assumes we want a picture (100/255) * 170 degrees wide
    // 100 is the value that's hard coded in
    
    int vertPWM = vertical  * 100 / height;
    int horizPWM = horizontal * 100 / width;
    analogWrite(horizPin, horizPWM);
    analogWrite(vertPin, vertPWM);
    delay(80);
    // delay 40ms
        
    return;
}

void writeBMPImage(int * input, char fileName[], int w, int h){
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
    char name[] = "img4.bmp";
    Serial.print("In the writeBMPImage, writing ");
    Serial.write(name);
    Serial.write("\n");
   
    

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

    // create image data; heavily modified version via:
    // http://stackoverflow.com/a/2654860
    unsigned char *img = NULL;                        // image data
    if (img) {                                                        // if there's already data in the array, clear it
        free(img);
    }
    img = (unsigned char *)malloc(3*w*h);

    for (int y=0; y<h; y++) {
        for (int x=0; x<w; x++) {
            int colorVal = input[y*w + x];            // classic formula for px listed in line
            //Serial.println(colorVal);
            img[(y*w + x)*3+0] = (unsigned char)(colorVal);        // R
            img[(y*w + x)*3+1] = (unsigned char)((255-colorVal)/2);        // G
            img[(y*w + x)*3+2] = (unsigned char)(255 - colorVal);        // B
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
    unsigned char bmpPad[rowSize - 3*w];
    for (int i=0; i<sizeof(bmpPad); i++) {                 // fill with 0s
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
        delay(2);
        //file.write(img+(w*(h-i-1)*3), 3*w);                                // write px data
        dataFile.write(bmpPad, (4-(w*3)%4)%4);                                 // and padding as needed
        delay(2);
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
