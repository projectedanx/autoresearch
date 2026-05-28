with open("tests/test_tactile_dialectician_simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'escrow.quarantined_modules["Module_X"], "[⊘] Mutually exclusive requirements")' in line:  # noqa: E501
        lines[i] = '            escrow.quarantined_modules["Module_X"],\n            "[⊘] Mutually exclusive requirements")\n'  # noqa: E501

with open("tests/test_tactile_dialectician_simulation.py", "w") as f:
    f.writelines(lines)
