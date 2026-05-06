with open("tests/test_tactile_dialectician_simulation.py", "r") as f:
    content = f.read()

# Make sure we don't have multiple TestTactileDialecticianV6Evaluator classes,
# which might happen if we accidentally copy pasted the original content into the file.  # noqa: E501
import re
print("Matches found:", len(re.findall(
    "class TestTactileDialecticianV6Evaluator", content)))
