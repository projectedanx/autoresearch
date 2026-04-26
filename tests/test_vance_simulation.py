import unittest
from vance_simulation import VANCETopologyEvaluator


class TestVANCETopologyEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = VANCETopologyEvaluator()

    def test_betti_1_cycle_detection(self):
        # Setup a circular dependency
        self.evaluator.add_node("A", "file:///src/module_a.py")
        self.evaluator.add_node("B", "file:///src/module_b.py")
        self.evaluator.add_node("C", "file:///src/module_c.py")

        self.evaluator.add_edge("A", "B", "IMPORTS")
        self.evaluator.add_edge("B", "C", "IMPORTS")

        self.assertFalse(self.evaluator.detect_betti_1_cycle())

        # Complete the cycle
        self.evaluator.add_edge("C", "A", "IMPORTS")

        self.assertTrue(self.evaluator.detect_betti_1_cycle())

    def test_mereological_bounding(self):
        # Setup nodes with a scope chain
        self.evaluator.add_node("Global", "file:///src/auth.rs", 0)
        self.evaluator.add_node("Class", "file:///src/auth.rs", 1)
        self.evaluator.add_node("Method", "file:///src/auth.rs", 2)
        self.evaluator.add_node("Variable", "file:///src/auth.rs", 3)

        self.evaluator.add_edge("Variable", "Method", "SCOPES_WITHIN")
        self.evaluator.add_edge("Method", "Class", "SCOPES_WITHIN")
        self.evaluator.add_edge("Class", "Global", "SCOPES_WITHIN")

        # Test valid path
        self.assertTrue(
            self.evaluator.check_mereological_bounds("Variable", "Class"))

        # Test invalid path
        self.assertFalse(self.evaluator.check_mereological_bounds(
            "Variable", "OtherClass"))

    def test_dccd_guard_and_nfl(self):
        required_fields = ["jsonrpc", "id", "result"]

        # Valid payload
        valid_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": "Success"
        }
        is_valid, reason = self.evaluator.dccd_guard(
            valid_payload, required_fields)
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
        self.assertEqual(len(self.evaluator.scars), 0)

        # Invalid payload
        invalid_payload = {
            "jsonrpc": "2.0",
            "result": "Success"
        }
        is_valid, reason = self.evaluator.dccd_guard(
            invalid_payload, required_fields)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field: id", reason)
        self.assertEqual(len(self.evaluator.scars), 1)
        self.assertEqual(
            self.evaluator.scars[0]["trigger"], "schema_validation")


if __name__ == '__main__':
    unittest.main()
