#include <phidget21.h>
#define ANGLE 45


int functionInSteppers();

int initStepper(CPhidgetStepperHandle stepper, int index, int serialNumber);
int gotoLocation(CPhidgetStepperHandle stepper, int index, int loc);
int gotoPixel(CPhidgetStepperHandle stepper, int index, int pixel, int width);
float readLocInDegrees(CPhidgetStepperHandle stepper, int width);
int gotoPixel2D(CPhidgetStepperHandle horizStepper, int indH, 
                CPhidgetStepperHandle vertStepper, int indV, 
                int horizPixel2, int width, int vertPixel2, int height);

void goDeltaAngle(CPhidgetStepperHandle stepper, float angle);
int haltStepper(CPhidgetStepperHandle stepper);

int fromSampleCode();
int gotoPixel2DandExit(CPhidgetStepperHandle horizStepper, int indH, 
                CPhidgetStepperHandle vertStepper, int indV, 
                int horizPixel2, int width, int vertPixel2, int height);

void setVelocity(CPhidgetStepperHandle stepper, float perc);
void setAcceleration(CPhidgetStepperHandle stepper, float perc);
