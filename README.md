mount linux build directory here

# Windows

Creating a symbolic link on Windows. The link folder must not exist. This links from the target to the link meaning that the files in target_folder show up in link_folder

```batch
mklink /D <link_folder> <target_folder>
```

## Example Use
`mklink /D "C:\Users\The Pigeon Lord 9000\Desktop\GPIO_Example_2\linux_build" \\192.168.56.2\shared_folder\GPIO_Example_2`