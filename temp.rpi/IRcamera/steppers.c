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

#include <stdio.h>
#include <stdlib.h>
#include <phidget21.h>

#define ANGLE 45
#define MAX_VEL 240
#define MIN_ACCEL 20323
#define WAIT_MS 28

int CCONV AttachHandler(CPhidgetHandle stepper, void *userptr){
    int serialNo;
    const char *name;

    CPhidget_getDeviceName (stepper, &name);
    CPhidget_getSerialNumber(stepper, &serialNo);
    printf("%s %10d attached!\n", name, serialNo);
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
    printf("Motor: %d > Current Position: %lld\n", Index, Value);
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
    serial = CPhidget_open((CPhidgetHandle)stepper, serialNumber);
    printf("serial: %d\n", serial);
    fflush(stdout);

    //get the program to wait for an stepper device to be attached
    printf("Waiting for Phidget to be attached....\n");
    if((result = CPhidget_waitForAttachment((CPhidgetHandle)stepper, 10000))){
        CPhidget_getErrorDescription(result, &err);
        printf("Problem waiting for attachment: %s\n", err);
        return 0;
    }

    //read event data
    printf("Reading accel/vel data.....\n");

    // This example assumes stepper motor is attached to index 0
    // Set up some initial acceleration and velocity values
    // minAccel defaults to minAccel: 46696
    // maxAccel defailts to maxVel: 46712

    CPhidgetStepper_getAccelerationMin(stepper, index, &minAccel);
    CPhidgetStepper_getVelocityMax(stepper, index, &maxVel);

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
    if(CPhidgetStepper_getCurrentPosition(stepper, index, &curr_pos) == EPHIDGET_OK)
        printf("Motor: 0 > Current Position: %lld\n", curr_pos);

    CPhidgetStepper_setCurrentPosition(stepper, index, 0);
    CPhidgetStepper_setEngaged(stepper, index, 1);
    printf("Done with init.\n");
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
    float loc = ANGLE * pixel / width; // in degrees
    loc = loc * (1200 * 16) / 360;   // deg * steps/deg
    gotoLocation(stepper, index, (int)loc);
}
int gotoPixel2D(CPhidgetStepperHandle horizStepper, CPhidgetStepperHandle vertStepper, 
    int horizPixel, int width, int vertPixel, int height){
    float horizLoc = ANGLE * horizPixel / width;
    horizLoc = horizLoc * (1200 * 16) / 360;
    float vertLoc = ANGLE * vertPixel / height;
    vertLoc = vertLoc * (1200 * 16) / 360;

    CPhidgetStepper_setTargetPosition(horizStepper, 0, horizLoc);
    CPhidgetStepper_setTargetPosition(vertStepper, 1, vertLoc);
    __int64 sendHorizLoc = (int)horizLoc;
    __int64 desired;
    __int64 current;
    float off;
    while(1){
        CPhidgetStepper_getCurrentPosition(horizStepper, 0, &sendHorizLoc);
        if((int)horizLoc == sendHorizLoc) break;

        off = abs(sendHorizLoc - horizLoc);
        if (off * 1000 < MAX_VEL *  WAIT_MS) break; 
        // breaks in enough time for WAIT_MS
    }

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




