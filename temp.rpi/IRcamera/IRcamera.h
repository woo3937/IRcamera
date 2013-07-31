
#include <phidget21.h>
#include "steppers.h"
#include "brain.h"

#define WIDTH 100
#define HEIGHT 100

#define WAIT_MS 46
#define SAME_IMAGE_FILE 1
#define MIN_TEMP 10
#define MAX_TEMP 60

void initIR();
float readTemp();
int readConfig();
void writeConfig();
void waitMillis(int millis);
void writeConfigParams( unsigned char command, unsigned char lsb,
                        unsigned char msb,     unsigned char pec);
void writeImage(char filename[50], float * data, int width, int height);
unsigned char findPec(unsigned char comm, unsigned char lsb, unsigned char msb);
