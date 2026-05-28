with open("tactile_dialectician_simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if len(line) > 80:
        if "Computes the density of nodes/edges representing query domain complexity." in line:  # noqa: E501
            lines[i] = "        Computes the density of nodes/edges representing query domain\n        complexity.\n"  # noqa: E501

with open("tactile_dialectician_simulation.py", "w") as f:
    f.writelines(lines)
