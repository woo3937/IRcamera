
int functionInSteppers();

int initStepper(CPhidgetStepperHandle stepper, int index, int serialNumber);
int gotoLocation(CPhidgetStepperHandle stepper, int index, int loc);
void haltStepper(CPhidgetStepperHandle stepper);
int gotoPixel(CPhidgetStepperHandle stepper, int index, int pixel, int width);
int gotoPixel2D(CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper, 
                int horizPixel, int width, int vertPixel, int height);
float readLocInDegrees(CPhidgetStepperHandle stepper, int width);

void fromSampleCode();


