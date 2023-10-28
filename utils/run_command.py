
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

script_directory = os.path.dirname(os.path.abspath(__file__))

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
  if sys.platform.startswith('linux'):        # Linux
    divider = "/"
  elif sys.platform.startswith('win'):        # Windows
    divider = "\\"

  with open(script_directory + divider + file_name, "r") as file:
    template = Template(file.read())

  data = {
    'BUILD_MACHINE_IP': '192.168.1.100',
  }

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

def parse_task_args(args):
  arg = ""
  for x in args:
    if isinstance(x, dict) and 'quote' in x:
      if x["quote"] == None:
        pass
      else:
        arg = arg + " '" + parse_task_args(x["quote"]) + "'"
    else:
      arg = arg + " " + x
  return arg




if __name__ == "__main__":
    main()




