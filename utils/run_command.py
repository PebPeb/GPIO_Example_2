
import os
from jinja2 import Template                 # For templating my .yaml files
import yaml
import sys
import glob

# Example.yaml
# Commands:
#   - command: ssh
#     args:
#       - dev@192.168.56.2
#       - quote:
#         - ls;
#         - ls;

# Global settings
script_directory = os.path.dirname(os.path.abspath(__file__))
if sys.platform.startswith('linux'):        # Linux
  divider = "/"
elif sys.platform.startswith('win'):        # Windows
  divider = "\\"


def main(): 
  if len(sys.argv) > 1: # If an argument
    yaml_files = glob.glob(os.path.join(script_directory, "*.yaml"))  
    yaml_files_without_extension = [os.path.splitext(os.path.basename(file))[0] for file in yaml_files]

    if sys.argv[1] in yaml_files_without_extension:
      task = parse_yaml(sys.argv[1] + ".yaml")
      execute(task)
    else:
      print("Task Not Found")
      print()
      print("-- Valid Tasks --")
      for x in yaml_files_without_extension:
        print(x)
      print()
      exit()

  else:
    print("No Task Provided")
    exit()


def parse_yaml(file_name):
  with open(script_directory + divider + file_name, "r") as file:
    template = Template(file.read())
  
  data = {}
  with open(script_directory + divider + ".." + divider + "program.conf", 'r') as file:
    for line in file:
    # Split each line into key and value using the '=' as a separator
      parts = line.strip().split("=")

      # Check if the line has a key-value pair
      if len(parts) == 2:
        key, value = parts
        data[key] = value

  for key, value in data.items():
      for key_1, value_1 in data.items():
          value = value.replace('${' + key_1 + '}', value_1)
      data[key] = value

  rendered_yaml = template.render(data)

  # Parse the YAML file
  #with open(script_directory + divider + file_name, "r") as file:
  task = yaml.safe_load(rendered_yaml)
  return task

def execute(task):
  commands = []
  for x in task["Commands"]:                              # Commands
    command = x["command"]                                # command
    if x["args"] == None:
      pass
    else:
      command = command + parse_task_args(x["args"])
    
    print(command)
    try:
      os.system(command)
    except:
      print("command failed")
      exit(-1)

def parse_task_args(args, first_quote=False):
  arg = ""
  for x in args:
    if isinstance(x, dict) and 'quote' in x:
      if x["quote"] == None:
        pass
      else:
        arg = arg + " \"" + parse_task_args(x["quote"], True) + "\""
    else:
      if first_quote:
        arg = arg + x
        first_quote = False
      else:
        arg = arg + " " + x
  return arg


if __name__ == "__main__":
    main()


