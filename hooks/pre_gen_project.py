import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.module_name }}"

if not re.match(MODULE_REGEX, module_name):
    print("ERROR: %s is not a valid Python module name!" % module_name)
    sys.exit(1)

use_r = "{{ cookiecutter.use_r }}"

if use_r == "yes":
    exit_code = os.system("Rscript -e 'quit(status = 0)'")
    if exit_code != 0:
        print("ERROR: R is not installed on your system. Please install R before proceeding.")
        sys.exit(1)
