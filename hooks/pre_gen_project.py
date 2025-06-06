import os
import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.module_name }}"

if not re.match(MODULE_REGEX, module_name):
    print("ERROR: %s is not a valid Python module name!" % module_name)
    sys.exit(1)

repo_url = "{{ cookiecutter.repo_url }}"

if repo_url:
    if not re.match(r"^(https://?|git@)", repo_url):
        print("ERROR: %s is not a valid git repository URL!" % repo_url)
        sys.exit(1)

    exit_code = os.system(f"git ls-remote {repo_url} > /dev/null 2>&1")
    if exit_code != 0:
        print("ERROR: The repository URL %s does not exist!" % repo_url)
        sys.exit(1)
