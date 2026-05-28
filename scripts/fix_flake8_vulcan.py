import subprocess
import re


def fix_flake8():
    result = subprocess.run(
        ["uvx", "flake8", "--exclude", ".venv"], capture_output=True, text=True)  # noqa: E501
    if result.returncode == 0:
        return

    files_to_fix = set()
    for line in result.stdout.splitlines():
        match = re.match(r"^([^:]+):", line)
        if match:
            files_to_fix.add(match.group(1))

    for file in files_to_fix:
        if file.startswith("./"):
            file = file[2:]
        if file.endswith(".py"):
            print(f"Fixing {file}")
            subprocess.run(["uvx", "autopep8", "--in-place", file])


if __name__ == "__main__":
    fix_flake8()
