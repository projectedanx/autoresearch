import sys

with open('train.py', 'r') as f:
    content = f.read()

search_string = """        self.ve_gate_channels = 32
        self.ve_gate = (
            nn.Linear(self.ve_gate_channels, self.n_kv_head, bias=False)
            if has_ve(layer_idx, config.n_layer) else None
        )"""

replace_string = """        self.ve_gate_channels = 32
        self.ve_gate = (
            nn.Linear(self.ve_gate_channels, self.n_kv_head, bias=False)
            if has_ve(layer_idx, config.n_layer)
            else None
        )"""

if search_string in content:
    content = content.replace(search_string, replace_string)
    with open('train.py', 'w') as f:
        f.write(content)
    print("Success")
else:
    print("Failed to find search string")
