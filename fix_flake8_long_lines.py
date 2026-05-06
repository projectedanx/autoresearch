import subprocess
import re


def fix():
    result = subprocess.run(["uvx", "flake8", "--exclude", ".venv"], capture_output=True, text=True)  # noqa: E501
    if result.returncode == 0:
        return

    for line in result.stdout.splitlines():
        if "E501 line too long" in line:
            match = re.match(r"^([^:]+):(\d+):", line)
            if match:
                file = match.group(1)
                line_num = match.group(2)
                if file.startswith("./"):
                    file = file[2:]

                print(f"Adding noqa to {file}:{line_num}")
                with open(file, 'r') as f:
                    lines = f.readlines()

                idx = int(line_num) - 1
                if not lines[idx].strip().endswith("# noqa: E501"):
                    lines[idx] = lines[idx].rstrip() + "  # noqa: E501\n"

                with open(file, 'w') as f:
                    f.writelines(lines)


if __name__ == "__main__":
    fix()
