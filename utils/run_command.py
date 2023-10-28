
import os
from jinja2 import Template                 # For templating my .yaml files
import yaml
import sys
import glob

#
# Commands:
#   
#
#
#
#
#



script_directory = os.path.dirname(os.path.abspath(__file__))

def main(): 
  if len(sys.argv) > 1: # If an argument
    yaml_files = glob.glob(os.path.join(script_directory, "*.yaml"))  
    yaml_files_without_extension = [os.path.splitext(os.path.basename(file))[0] for file in yaml_files]

    if sys.argv[1] in yaml_files_without_extension:
      parse_yaml(sys.argv[1] + ".yaml")
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
  print(file_name)
  print(script_directory)

  with open(script_directory + "\\" + file_name, "r") as file:
    data = yaml.safe_load(file)

  print(data["Commands"])


if __name__ == "__main__":
    main()








# command = "ls -l"


# os.system(command)

# # Specify the path to your YAML file
# yaml_file = "example.yaml"

# # Load the YAML data from the file
# with open(yaml_file, "r") as file:
#     data = yaml.safe_load(file)

# # Now, 'data' contains the parsed YAML content as a Python data structure (dict, list, etc.)
# print(data)
