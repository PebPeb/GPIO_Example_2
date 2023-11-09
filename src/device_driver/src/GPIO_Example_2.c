/*
 *  hello-1.c - The simplest kernel module
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/kdev_t.h>
#include <linux/io.h>

#include "linux/GPIO-fs.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Bryce Keen");

#define DRIVER_NAME "GPIO_Example_2"

// Global Vars
static int          major_num;
static int          num_devices = 1;
static struct cdev  GPIO_Example_2_cdev; 
struct class       *GPIO_Example_2_class;
struct device      *GPIO_Example_2_device;

void __iomem *device_memory;

// Define the physical address of the device
resource_size_t device_phys_addr = 0x41200000;


// Function declarations
static int device_open(struct inode *inode, struct file *file);
static long device_ioctl(struct file *filp, unsigned int cmd, unsigned long arg);
static int device_release(struct inode *inode, struct file *file);

static struct file_operations fops = { 
  .owner = THIS_MODULE,
  .unlocked_ioctl = device_ioctl, 
  .open = device_open, 
  .release = device_release,              /* a.k.a. close */ 
}; 

static int calledi = 0;
static long device_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
  calledi += 1;
  printk(KERN_INFO "IOCTL called %d\n", calledi);


  device_memory = ioremap(device_phys_addr, 4096);
  if (!device_memory) {
      pr_err("Failed to map device memory.\n");
      return -ENOMEM;                         // Out of memory
  }

  switch(cmd)
  {
    case GPIO_CMD_SET_LED:
      struct GPIO_args data;
      if (copy_from_user(&data, (const void*)arg, sizeof(data))) {
        return -1;
      } else {
        printk(KERN_INFO "Set LED %d\n", data.LED);
        iowrite32(data.LED, device_memory);
      }

      break;
    default:
      iounmap(device_memory);
      return -1;
      break;
  }
  iounmap(device_memory);
  return 0;
}

static int device_open(struct inode *inode, struct file *file) 
{ 
  pr_info("device_open(%p)\n", file); 

  try_module_get(THIS_MODULE); 
  return 0; 
} 

static int device_release(struct inode *inode, struct file *file) 
{ 
  pr_info("device_release(%p,%p)\n", inode, file); 

  module_put(THIS_MODULE); 
  return 0; 
} 


static int __init init_GPIO_Example_2(void) {
  printk(KERN_INFO "Initializing GPIO Example 2.\n");

  dev_t dev;

  if(alloc_chrdev_region(&dev, 0, num_devices, DRIVER_NAME))
    goto error;
  cdev_init(&GPIO_Example_2_cdev, &fops);
  if(cdev_add(&GPIO_Example_2_cdev, dev, num_devices))
    goto error;

  major_num = MAJOR(dev);

  GPIO_Example_2_class = class_create(THIS_MODULE, DRIVER_NAME);
  GPIO_Example_2_device = device_create(GPIO_Example_2_class, NULL, dev, NULL, DRIVER_NAME);

  return 0;

error:
  printk(KERN_INFO "ERROR Initializing GPIO Example 2\n");
  return -1;
}

static void __exit cleanup_GPIO_Example_2(void) {
  printk(KERN_INFO "Destroying GPIO Example 2.\n");

  dev_t dev = MKDEV(major_num, 0);

  device_destroy(GPIO_Example_2_class, dev); 
  class_destroy(GPIO_Example_2_class); 

  cdev_del(&GPIO_Example_2_cdev); 
  unregister_chrdev_region(dev, num_devices); 
  pr_alert("%s driver removed.\n", DRIVER_NAME); 
}


module_init(init_GPIO_Example_2);
module_exit(cleanup_GPIO_Example_2);
