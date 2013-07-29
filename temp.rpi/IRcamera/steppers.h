
int functionInSteppers();

int initStepper(CPhidgetStepperHandle stepper, int index, int serialNumber);
int gotoLocation(CPhidgetStepperHandle stepper, int index, int loc);
void haltStepper(CPhidgetStepperHandle stepper);
int gotoPixel(CPhidgetStepperHandle stepper, int index, int pixel, int width);
float readLocInDegrees(CPhidgetStepperHandle stepper, int width);
int gotoPixel2D(CPhidgetStepperHandle horizStepper, int indH, 
                CPhidgetStepperHandle vertStepper, int indV, 
                int horizPixel2, int width, int vertPixel2, int height);

void fromSampleCode();
void goDeltaAngle(CPhidgetStepperHandle stepper, float angle);


