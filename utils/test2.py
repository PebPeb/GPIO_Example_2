import os
import sys

if sys.platform.startswith('linux'):        # Linux
    divider = "/"
elif sys.platform.startswith('win'):        # Windows
    divider = "\\"

config = {}

script_directory = os.path.dirname(os.path.abspath(__file__))
with open(script_directory + divider + ".." + divider + "program.conf", 'r') as file:
    for line in file:
        # Split each line into key and value using the '=' as a separator
        parts = line.strip().split("=")
        
        # Check if the line has a key-value pair
        if len(parts) == 2:
            key, value = parts
            config[key] = value

for key, value in config.items():
    for key_1, value_1 in config.items():
        value = value.replace('${' + key_1 + '}', value_1)
    config[key] = value
