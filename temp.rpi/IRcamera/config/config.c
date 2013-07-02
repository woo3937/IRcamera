#include <stdlib.h>
#include <stdio.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>


#define ADDRESS 0x5A
#define COMMAND 0x25
#define LSB 0x74
#define MSB 0xB4
#define PEC 0x70

int main(){
    int fd;
    fd = open( "/dev/i2c-1", O_RDWR );
    printf("In the function...\n");
    if( ioctl( fd, I2C_SLAVE, ADDRESS ) < 0 ){
            fprintf( stderr, "Failed to set slave address: %m\n" );
            printf("Yup, it failed.");
            return 2;
    }
    __u8 * write = (__u8 *)malloc(sizeof(__u8) * 4);
    /*write[0] = COMMAND;*/
    write[0] = LSB;
    write[1] = MSB;
    write[2] = PEC;
    for (int i=0; i<10; i++){
        i2c_smbus_write_block_data(fd, (__u8)COMMAND, 4, write);
        i2c_smbus_write_i2c_block_data(fd, (__u8)COMMAND, 4, write);
    }


    return 0;
}
