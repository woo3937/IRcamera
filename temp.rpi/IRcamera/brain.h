#include <phidget21.h>

void FISTA(float * xold, float * xold1, float * y, int * idx, 
           int width, int height, float p, float tn, float tn1, int its);
void dumbCamera(int width, int height,
        CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper);
void mainIST(int width, int height,
        CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper);
