/*
 *  hello-1.c - The simplest kernel module
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Bryce Keen");


static int __init init_mymodule(void) {
  printk(KERN_INFO "Hello world 1.\n");

  return 0;
}

static void __exit cleanup_mymodule(void) {
  printk(KERN_INFO "Goodbye world 1.\n");

}


module_init(init_mymodule);
module_exit(cleanup_mymodule);
