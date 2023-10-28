import re
import os
import sys

if sys.platform.startswith('linux'):        # Linux
    divider = "/"
elif sys.platform.startswith('win'):        # Windows
    divider = "\\"

# Initialize a dictionary to store the variables
variables = {}

# Function to evaluate expressions like VERSION=${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH}
def evaluate_expression(match):
    expr = match.group(0)
    var_name = expr.split('=')[0]
    var_value = expr.split('=')[1]
    print(variables.items())
    for key, value in variables.items():
        print(var_value)
        print()
        var_value = var_value.replace('${' + key + '}', str(value))
    return f"{var_name}={var_value}"

# Read the input file
script_directory = os.path.dirname(os.path.abspath(__file__))
with open(script_directory + divider + ".." + divider + "program.conf", 'r') as file:
    content = file.read()

# Use regular expressions to find variable assignments and evaluate expressions
pattern = re.compile(r'^[A-Z_][A-Z_0-9]*=[\s\S]*?(?=\n[A-Z_]|$)', re.MULTILINE)
content = re.sub(pattern, evaluate_expression, content)

# Split the lines and store the variable assignments in the variables dictionary
lines = content.split('\n')
for line in lines:
    if '=' in line:
        parts = line.split('=')
        var_name = parts[0]
        var_value = parts[1]
        variables[var_name] = var_value

# Print the variables
for var_name, var_value in variables.items():
    print(f"{var_name} = {var_value}")
