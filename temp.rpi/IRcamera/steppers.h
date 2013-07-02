
int functionInSteppers();

int initStepper(CPhidgetStepperHandle stepper);
int gotoLocation(CPhidgetStepperHandle stepper, int loc);
void haltStepper(CPhidgetStepperHandle stepper);
int gotoPixel(CPhidgetStepperHandle stepper, int pixel, int width);
int gotoPixel2D(CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper, 
                int horizPixel, int width, int vertPixel, int height);

void fromSampleCode();


