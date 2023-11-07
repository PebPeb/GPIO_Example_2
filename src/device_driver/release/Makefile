
obj-m := GPIO_Example_2.o

# KERNEL_SRC := /home/dev/Documents/petalinux_projects/GPIO_Example_2/build/tmp/work/zynq_generic-xilinx-linux-gnueabi/linux-xlnx/5.15.19+gitAUTOINC+b0c1be301e-r0/linux-zynq_generic-standard-build/ 
# CROSS_COMPILE := /home/dev/Documents/petalinux_projects/GPIO_Example_2/build/tmp/work/zynq_generic-xilinx-linux-gnueabi/linux-xlnx/5.15.19+gitAUTOINC+b0c1be301e-r0/recipe-sysroot-native/usr/bin/arm-xilinx-linux-gnueabi/arm-xilinx-linux-gnueabi-
KERNEL_SRC := /home/dev/Documents/petalinux_projects/GPIO_zybo/build/tmp/work/zynq_generic-xilinx-linux-gnueabi/linux-xlnx/5.15.19+gitAUTOINC+b0c1be301e-r0/linux-zynq_generic-standard-build/ 
CROSS_COMPILE := /home/dev/Documents/petalinux_projects/GPIO_zybo/build/tmp/work/zynq_generic-xilinx-linux-gnueabi/linux-xlnx/5.15.19+gitAUTOINC+b0c1be301e-r0/recipe-sysroot-native/usr/bin/arm-xilinx-linux-gnueabi/arm-xilinx-linux-gnueabi-
ARCH := arm

MY_CFLAGS += -g -DDEBUG
ccflags-y += ${MY_CFLAGS}

SRC := $(shell pwd)

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install

clean:
	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c *.mod
	rm -f Module.markers Module.symvers modules.order
	rm -rf .tmp_versions Modules.symvers
