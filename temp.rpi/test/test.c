
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <fcntl.h>  
#include <errno.h>  
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>

#include <string.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>

#include <linux/i2c-dev.h>

/*#define MAG_ADDRESS        (0x >> 1)  */
#define MAG_ADDRESS 0x5A
#define LSM303_WHO_AM_I_M  (0x0F) 

int main(){
    int x = 1;
    char buf[10];
    i2c_rdwr_ioctl_data  msgset; 

    const char * bufName = "/dev/i2c-1";
    int file = open(bufName, O_RDWR);

    ioctl(file,I2C_RDWR,(unsigned long)&msgset);
  
    return 0; 

}







