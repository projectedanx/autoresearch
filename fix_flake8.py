with open("tactile_dialectician_simulation.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if len(line) > 80:
        if "def calculate_geometric_density_score(self, nodes: int, edges: int) -> float:" in line:
            lines[i] = "    def calculate_geometric_density_score(\n            self, nodes: int, edges: int) -> float:\n"

with open("tactile_dialectician_simulation.py", "w") as f:
    f.writelines(lines)
