import os
import re
import shutil
import subprocess
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


def _gh(*args: str) -> tuple[int, str]:
    """Run a `gh` subcommand, returning its (returncode, stripped stdout)."""
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip()


# When auto_configure == "yes" the post-gen hook runs `gh repo create <org>/<repo>`. We want to validate up front that
# gh is installed and authenticated, and that `org` is one the user can create repos under OR is the user's personal
# account name.
auto_configure = "{{ cookiecutter.auto_configure }}"
org = "{{ cookiecutter.org }}".strip()

if auto_configure == "yes":
    if shutil.which("gh") is None:
        print(
            "ERROR: 'gh' (GitHub CLI) is not installed, but auto_configure='yes' needs it.\n"
            "Install it from https://cli.github.com/, or choose auto_configure='local' to skip GitHub setup."
        )
        sys.exit(1)

    if not org:
        print("ERROR: 'org' must not be empty when auto_configure='yes'.")
        sys.exit(1)

    auth_rc, _ = _gh("auth", "status")
    if auth_rc != 0:
        print("ERROR: 'gh' is not authenticated. Run 'gh auth login' and then re-run the cookiecutter.")
        sys.exit(1)

    user_rc, username = _gh("api", "user", "--jq", ".login")
    if user_rc != 0 or not username:
        print("ERROR: Could not determine your GitHub username via 'gh'. Check 'gh auth status' and try again.")
        sys.exit(1)

    if org.casefold() != username.casefold():
        orgs_rc, orgs_out = _gh("api", "--paginate", "user/orgs", "--jq", ".[].login")
        member_orgs = orgs_out.splitlines() if orgs_rc == 0 else []

        if org.casefold() not in {o.casefold() for o in member_orgs}:
            state_rc, state = _gh("api", f"user/memberships/orgs/{org}", "--jq", ".state")
            if not (state_rc == 0 and state == "active"):
                available = ", ".join([username, *member_orgs])
                print(
                    f"ERROR: GitHub account '{username}' cannot create repositories under org '{org}'.\n"
                    f"You are not an authenticated member of '{org}'. Set 'org' to one you can access: {available}.\n"
                    "(Or your own username for a personal repository, or choose auto_configure='local' to skip.)"
                )
                sys.exit(1)
