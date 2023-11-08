
// STD includes
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>

// Program Level includes
#include "linux/GPIO-fs.h"


int main() {
    int fd = open("/dev/GPIO_Example_2", O_RDWR); // Replace "/dev/your_device" with the actual device file path

    if (fd < 0) {
        perror("Failed to open device file");
        exit(EXIT_FAILURE);
    }

    struct GPIO_args data;
    data.LED = 0x3;

    int ioctl_result = ioctl(fd, GPIO_CMD_SET_LED, &data); // Replace YOUR_IOCTL_COMMAND with the actual IOCTL command number

    if (ioctl_result < 0) {
        perror("IOCTL failed");
        close(fd);
        exit(EXIT_FAILURE);
    }

    // Process the result from the IOCTL operation

    close(fd);
    return 0;
}
