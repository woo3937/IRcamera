#include <phidget21.h>

void FISTA(float * xold, float * xold1, float * y, int * idx, 
           int width, int height, float p, float tn, float tn1, int its);
void dumbCamera(int width, int height,
        CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper);
void mainIST(int width, int height,
        CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper);
float testWaitTime(int its, int start);
float std(float * array, int N);
float testNoise(int its, int wait);
void getMeasurementsFromBranch(CPhidgetStepperHandle horizStepper, 
                               CPhidgetStepperHandle vertStepper,
                               float * xold, int wait_ms,
                               int minY, int maxY, int minX, int maxX, 
                               float rate, int width, int height);
