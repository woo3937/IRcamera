/* The stepper motors are at this URL:
 *     http://www.phidgets.com/products.php?category=23&product_id=3317_1
 * The 1067 driver board at this URL:
 *     http://www.phidgets.com/products.php?product_id=1067
 *     For the 1067, the User Guide is fanastic.
 *
 * The stepper motors have four wires: red, green, black and blue.
 *
 * My setup, with the wires:
 *     | A   | B    | C     | D     |
 *     |-----|------|-------|-------|
 *     | red | blue | black | green |
 *
 *  --Scott Sievert (sieve121@umn.edu), 2013-06-26
 *
 *  TODO: get rid of the while-loop in gotoLocation. We want to have the sensor
 *  be settling while we're moving to a location. --2013-06-27
 */
/* for a 32x32 image...
 *  p=0.5:  58.34s
 *  p=1.0: 105.89s
 *
 *  we're right at the limit for the speed our motors can do. it has to go
 *  farther for p=0.5, the reason 2*58 > 105.
 *
 * --Scott Sievert, 2013-08-1
 */

#include <stdio.h>
#include <stdlib.h>
#include <phidget21.h>
#include <math.h>
#include "steppers.h"

/*#define ANGLE 22*/
#define MAX_VEL 1000
#define MIN_ACCEL 20323
#define WAIT_MS 28

int CCONV AttachHandler(CPhidgetHandle stepper, void *userptr){
    int serialNo;
    const char *name;

    CPhidget_getDeviceName (stepper, &name);
    CPhidget_getSerialNumber(stepper, &serialNo);
    printf("%s %10d attached! -- and ", name, serialNo);
    return 0;
}

int CCONV DetachHandler(CPhidgetHandle stepper, void *userptr){
    int serialNo;
    const char *name;

    CPhidget_getDeviceName (stepper, &name);
    CPhidget_getSerialNumber(stepper, &serialNo);
    printf("%s %10d detached!\n", name, serialNo);

    return 0;
}
int CCONV ErrorHandler(CPhidgetHandle stepper, void *userptr, int ErrorCode, const char *Description){
    printf("Error handled. %d - %s\n", ErrorCode, Description);
    return 0;
}
int CCONV PositionChangeHandler(CPhidgetStepperHandle stepper, void *usrptr, int Index, __int64 Value){
   /*printf("Motor: %d > Current Position: %lld\n", Index, Value);*/
    return 0;
}

int initStepper(CPhidgetStepperHandle stepper, int index, int serialNumber){
    int result;
    __int64 curr_pos;
    const char *err;
    double minAccel, maxVel;
    int stopped;
 

    //Set the handlers to be run when the device is 
    // plugged in or opened from software, unplugge 
    // or closed from software, or generates an error.
    CPhidget_set_OnAttach_Handler((CPhidgetHandle)stepper, AttachHandler, NULL);
    CPhidget_set_OnDetach_Handler((CPhidgetHandle)stepper, DetachHandler, NULL);
    CPhidget_set_OnError_Handler((CPhidgetHandle)stepper, ErrorHandler, NULL);

    // Registers a callback that will run when the motor position is changed.
    // Requires the handle for the Phidget, the function that will be called, 
    // and an arbitrary pointer that will be supplied to the callback function (may be NULL).
    CPhidgetStepper_set_OnPositionChange_Handler(stepper, PositionChangeHandler, NULL);

    //open the device for connections
    int serial = -1;
    serial = CPhidget_open((CPhidgetHandle)stepper, -1);
    /*printf("serial: %d\n", serial);*/
    fflush(stdout);

    //get the program to wait for an stepper device to be attached
    /*printf("Waiting for Phidget to be attached....\n");*/
    if((result = CPhidget_waitForAttachment((CPhidgetHandle)stepper, 10000))){
        CPhidget_getErrorDescription(result, &err);
        printf("Problem waiting for attachment: %s\n", err);
        return 0;
    }

    //read event data
    /*printf("Reading accel/vel data.....\n");*/

    // This example assumes stepper motor is attached to index 0
    // Set up some initial acceleration and velocity values
    // minAccel defaults to minAccel: 46696
    // maxAccel defailts to maxVel: 46712

    CPhidgetStepper_getAccelerationMin(stepper, index, &minAccel);
    CPhidgetStepper_getVelocityMax(stepper, index, &maxVel);
    /*printf("Max Velocity: %f, min accel: %f\n", maxVel, minAccel);*/

    /*printf("maxVel: %d, minAccel: %d\n", maxVel, minAccel);*/
    /*int mul = 1000;*/
    /*maxVel   = mul * maxVel;*/
    /*minAccel = mul * minAccel;*/
    /*printf("maxVel: %d, minAccel: %d\n", maxVel, minAccel);*/

    /*CPhidgetStepper_setAcceleration(stepper, 0, minAccel*2);*/
    /*CPhidgetStepper_setVelocityLimit(stepper, 0, maxVel/2);*/
    CPhidgetStepper_setAcceleration(stepper, index, MIN_ACCEL*2);
    CPhidgetStepper_setVelocityLimit(stepper, index, MAX_VEL/2);
    /*CPhidgetStepper_getAccelerationMin(stepper, 0, &minAccel);*/
    /*CPhidgetStepper_getVelocityMax(stepper, 0, &maxVel);*/
    /*printf("minAccel: %d \n", minAccel); */
    /*printf("maxVel: %d\n", maxVel);*/

    //display current motor position if available
    if(CPhidgetStepper_getCurrentPosition(stepper, index, &curr_pos) == EPHIDGET_OK){
        /*printf("Motor: 0 > Current Position: %lld\n", curr_pos);*/
        printf("EPHIDGET_OK\n");
    }

    CPhidgetStepper_setCurrentPosition(stepper, index, 0);
    CPhidgetStepper_setEngaged(stepper, index, 1);
    /*printf("Done with init.\n");*/
}
int gotoLocation(CPhidgetStepperHandle stepper, int index, int loc){
    // TODO: speed optimizations can occur here. we need to get rid of the
    // while-loop and have the sensor be settling while we're going to a
    // location.
    __int64 finalPosition = loc;
    CPhidgetStepper_setTargetPosition(stepper, index, loc);
    while(1){
        // now, location changes (which makes no sense)
        CPhidgetStepper_getCurrentPosition(stepper, index, &finalPosition);
        if(finalPosition == loc) break;
        /*printf("pos: %d, loc: %d, is it waiting?\n", finalPosition, loc);*/
        /*printf("%d\n", position);*/
        /*if (position == loc) break;*/
    }
}
int gotoPixel(CPhidgetStepperHandle stepper, int index, int pixel, int width){
    // what angle do we want to go to?
    float loc = ANGLE * (float)(pixel) / (float)(width); // in degrees
    /*printf("what deg? %f\n", loc);*/
    // what location gives that angle?
    loc = loc * (1200 * 16) / 360.0f;   // deg * steps/deg
    /*printf("current loc: %.0f\n", loc);*/
    /*printf("loc: %f\n", loc);*/
    gotoLocation(stepper, index, (int)loc);
}
// gotoPixel2D does not exit early to allow the IR sensor to settle
int gotoPixel2D(CPhidgetStepperHandle horizStepper, int indH, 
                CPhidgetStepperHandle vertStepper, int indV, 
                int horizPixel2, int width, int vertPixel2, int height){
    __int64 horizPixel = (__int64)horizPixel2;
    __int64 vertPixel = (__int64)vertPixel2;
    float horizLoc = ANGLE * horizPixel / width;
    horizLoc = horizLoc * (1200 * 16) / 360;
    float vertLoc = ANGLE * vertPixel / height;
    vertLoc = vertLoc * (1200 * 16) / 360;

    CPhidgetStepper_setTargetPosition(horizStepper , indH , (__int64)horizLoc);
    CPhidgetStepper_setTargetPosition(vertStepper  , indV , (__int64)vertLoc);
    __int64 sendHorizLoc = (__int64)horizLoc;
    __int64 sendVertLoc = (__int64)vertLoc;
    __int64 desired;
    __int64 current;
    // off, offHorizontal, offVertical, offTotal
    float off, offH, offV, offT;
    while(1){
        CPhidgetStepper_getCurrentPosition(horizStepper, indH, &sendHorizLoc);
        CPhidgetStepper_getCurrentPosition(vertStepper, indV, &sendVertLoc);
        /*if((int)horizLoc == sendHorizLoc && (int)vertLoc == sendVertLoc) break;*/
        /*if((__int64)horizLoc == sendHorizLoc) break;*/
        /*if((__int64)vertLoc == sendVertLoc) break;*/
        /*printf("%lld, %lld, ", (__int64)vertLoc, sendVertLoc);*/
        /*printf("%lld, %lld\n", (__int64)horizLoc, sendHorizLoc);*/
        if((__int64)vertLoc == sendVertLoc && (__int64)horizLoc == sendHorizLoc) break;
        /*printf("%d\n", sendHorizLoc);*/

        /*offH = horizLoc - sendHorizLoc;*/
        /*offV = vertLoc - sendVertLoc;*/
        /*offT = sqrt(offH*offH + offV*offV);*/

        /*printf("offT %f\n", offT);*/
        /*if (offT < WAIT_MS * 1000 * MAX_VEL) break;*/

        /*if (off * 1000 < MAX_VEL *  WAIT_MS) break; */
        // breaks in enough time for WAIT_MS
    }
}
// gotoPixel2D DOES exit early to allow the IR sensor to settle
int gotoPixel2DandExit(CPhidgetStepperHandle horizStepper, int indH, 
                CPhidgetStepperHandle vertStepper, int indV, 
                int horizPixel2, int width, int vertPixel2, int height, int wait_ms){
    __int64 horizPixel = (__int64)horizPixel2;
    __int64 vertPixel = (__int64)vertPixel2;
    float horizLoc, vertLoc;

    horizLoc = ANGLE * horizPixel2 / (width * 1.0);
    horizLoc = horizLoc * (1200 * 16) / 360;

    vertLoc = ANGLE * vertPixel2 / (height * 1.0);
    vertLoc = vertLoc * (1200 * 16) / 360;

    CPhidgetStepperHandle stepper;

    CPhidgetStepper_setTargetPosition(horizStepper , indH , (__int64)horizLoc);
    CPhidgetStepper_setTargetPosition(vertStepper  , indV , (__int64)vertLoc);
    __int64 sendHorizLoc = (__int64)horizLoc;
    __int64 sendVertLoc = (__int64)vertLoc;
    __int64 desired;
    __int64 current;
    // off, offHorizontal, offVertical, offTotal
    float off, offH, offV, offT;
    double vel = -1;
    while(1){
        CPhidgetStepper_getCurrentPosition(horizStepper, indH, &sendHorizLoc);
        CPhidgetStepper_getCurrentPosition(vertStepper, indV, &sendVertLoc);

        if((__int64)vertLoc == sendVertLoc && (__int64)horizLoc == sendHorizLoc) {
            break;
        }
        
        offH = abs(horizLoc - sendHorizLoc);
        offV = abs(vertLoc - sendVertLoc);
        if(offH > offV){
            off = offH;
            stepper = horizStepper;
        }
        else{
            off = offV;
            stepper = vertStepper;
        }
        CPhidgetStepper_getVelocity(stepper, 0, &vel);
        vel = abs(vel);
        if (1000 * off <= wait_ms * vel){
            break;
        }
    }
}

float readLocInDegrees(CPhidgetStepperHandle stepper, int width){
    __int64 curr_pos = -1;
    CPhidgetStepper_getCurrentPosition(stepper, 0, &curr_pos);
    /*printf("curr_pos: %lld\n", curr_pos);*/
    float degrees = curr_pos * (float)360 / (float)(1200 * 16 * 1);
    /*printf("in readLocInDegrees: %f\n", degrees);*/
    return degrees;
}

int haltStepper(CPhidgetStepperHandle stepper){
    printf("in halt!\n");
    int stopped;
    stopped = PFALSE;
    while(!stopped){
        CPhidgetStepper_getStopped(stepper, 0, &stopped);
        //usleep(100000);
    }

    CPhidgetStepper_setEngaged(stepper, 0, 0);


    // since user input has been read, this is a signal to terminate the program so 
    // we will close the phidget and delete the object we created
    printf("Closing...\n");
    CPhidget_close((CPhidgetHandle)stepper);
    CPhidget_delete((CPhidgetHandle)stepper);

    //all done, exit
    return 0;
}
void goDeltaAngle(CPhidgetStepperHandle stepper, float angle){
    float loc = angle; //ANGLE * (float)(pixel) / (float)(width); // in degrees
    // what location gives that angle?
    loc = loc * (1200 * 16) / 360.0f;   // deg * steps/deg
    /*printf("current loc: %.0f\n", loc);*/
    /*printf("loc: %f\n", loc);*/

    // go to that location, first setting current loc
    int index = 0;
    CPhidgetStepper_setCurrentPosition(stepper, 0, 0);
    gotoLocation(stepper, index, (int)loc);
}

void setVelocity(CPhidgetStepperHandle stepper, float perc){
    double velocity = (double)(250e3 * perc);
    CPhidgetStepper_setVelocityLimit(stepper, 0, velocity/1);
}

void setAcceleration(CPhidgetStepperHandle stepper, float perc){
    double acceleration = (double)(10e6 * perc);
    CPhidgetStepper_setAcceleration(stepper, 0, acceleration*1);
}

int fromSampleCode(){
    // from the sample code (Stepper-simple.c)
    int result;
    __int64 curr_pos;
    const char *err;
    double minAccel, maxVel;
    int stopped;

    //Declare an stepper handle
    CPhidgetStepperHandle stepper = 0;

    //create the stepper object
    CPhidgetStepper_create(&stepper);

    //Set the handlers to be run when the device is 
    // plugged in or opened from software, unplugge 
    // or closed from software, or generates an error.
    CPhidget_set_OnAttach_Handler((CPhidgetHandle)stepper, AttachHandler, NULL);
    CPhidget_set_OnDetach_Handler((CPhidgetHandle)stepper, DetachHandler, NULL);
    CPhidget_set_OnError_Handler((CPhidgetHandle)stepper, ErrorHandler, NULL);

    // Registers a callback that will run when the motor position is changed.
    // Requires the handle for the Phidget, the function that will be called, 
    // and an arbitrary pointer that will be supplied to the callback function (may be NULL).
    CPhidgetStepper_set_OnPositionChange_Handler(stepper, PositionChangeHandler, NULL);

    //open the device for connections
    CPhidget_open((CPhidgetHandle)stepper, -1);

    //get the program to wait for an stepper device to be attached
    printf("Waiting for Phidget to be attached....");
    if((result = CPhidget_waitForAttachment((CPhidgetHandle)stepper, 10000))){
        CPhidget_getErrorDescription(result, &err);
        printf("Problem waiting for attachment: %s\n", err);
        return 0;
    }

    //read event data
    printf("Reading.....\n");

    // This example assumes stepper motor is attached to index 0
    // Set up some initial acceleration and velocity values
    // minAccel defaults to minAccel: 46696
    // maxAccel defailts to maxVel: 46712

    CPhidgetStepper_getAccelerationMin(stepper, 0, &minAccel);
    CPhidgetStepper_getVelocityMax(stepper, 0, &maxVel);

    maxVel = 16 * maxVel;
    minAccel = 16 * minAccel;

    CPhidgetStepper_setAcceleration(stepper, 0, minAccel*2);
    CPhidgetStepper_setVelocityLimit(stepper, 0, maxVel/2);
    printf("minAccel: %d\n", minAccel);
    printf("maxVel: %d\n", maxVel);

    //display current motor position if available
    if(CPhidgetStepper_getCurrentPosition(stepper, 0, &curr_pos) == EPHIDGET_OK)
        printf("Motor: 0 > Current Position: %lld\n", curr_pos);

    //keep displaying stepper event data until user input is read
    printf("Press any key to continue\n");
    getchar();

    //change the motor position
    //we'll set it to a few random positions to move it around

    //Step 1: Position 0 - also engage stepper
    printf("Set to position 0 and engage. Press any key to Continue\n");
    getchar();

    CPhidgetStepper_setCurrentPosition(stepper, 0, 0);
    CPhidgetStepper_setEngaged(stepper, 0, 1);

    //Step 2: Position 200
    printf("Move to position 200. Press any key to Continue\n");
    getchar();

    CPhidgetStepper_setTargetPosition (stepper, 0, 200);

    //Step 3: Position -1200
    printf("Move to position -1200. Press any key to Continue\n");
    getchar();

    CPhidgetStepper_setTargetPosition (stepper, 0, -1200);

    //Step 4: Set to 0, wait for it to reach position, Disengage
    printf("Reset to 0 and disengage motor. Press any key to Continue\n");
    getchar();

    CPhidgetStepper_setTargetPosition(stepper, 0, 0);

    stopped = PFALSE;
    while(!stopped){
        CPhidgetStepper_getStopped(stepper, 0, &stopped);
        //usleep(100000);
    }

    CPhidgetStepper_setEngaged(stepper, 0, 0);

    printf("Press any key to end\n");
    getchar();

    //since user input has been read, this is a signal to terminate the program so we will close the phidget and delete the object we created
    printf("Closing...\n");
    CPhidget_close((CPhidgetHandle)stepper);
    CPhidget_delete((CPhidgetHandle)stepper);

    //all done, exit
    return 0;
}




