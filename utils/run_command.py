
import os
from jinja2 import Template                 # For templating my .yaml files
import yaml
import sys
import glob
import argparse

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

  parser = argparse.ArgumentParser(description="Executes .yaml command structure that builds up a task")
  
  parser.add_argument("default_argument", nargs="?", default="", help="Task to execute")
  parser.add_argument("-p", "--print", action="store_true", help="Turn on print")

  args = parser.parse_args()

  yaml_files = glob.glob(os.path.join(script_directory, "*.yaml"))  
  yaml_files_without_extension = [os.path.splitext(os.path.basename(file))[0] for file in yaml_files]
  
  if not(args.default_argument == ""): # If an argument
    if args.default_argument in yaml_files_without_extension:
      task = parse_yaml(args.default_argument + ".yaml")
      if args.print:
        execute(task, True)
      else:
        execute(task)
    else:
      print("Task Not Found\n")
      print("-- Valid Tasks --")
      for x in yaml_files_without_extension:
        print(x)
      print()
      exit()
  else:
    print("No Task Provided\n")
    print("-- Valid Tasks --")
    for x in yaml_files_without_extension:
      print(x)
    print()
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

def execute(task, print_task=False):
  commands = []
  for x in task["Commands"]:                              # Commands
    command = x["command"]                                # command
    if x["args"] == None:
      pass
    else:
      command = command + parse_task_args(x["args"])
    try:
      if (print_task):
        print(command)
      else:
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


