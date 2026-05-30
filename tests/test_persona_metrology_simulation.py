import unittest
import pytest
from persona_metrology_simulation import PersonaMetrologyEvaluator


class TestPersonaMetrologyEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = PersonaMetrologyEvaluator()

    def test_spatial_bind_disconnected(self):
        relation = self.evaluator.enforce_spatial_bind(10.0, 5.0)
        self.assertEqual(relation, "DC")

    def test_spatial_bind_externally_connected(self):
        relation = self.evaluator.enforce_spatial_bind(
            10.0, 9.9, tolerance=0.15)
        self.assertEqual(relation, "EC")

    def test_spatial_bind_partial_overlap(self):
        relation = self.evaluator.enforce_spatial_bind(
            9.9, 10.0, tolerance=0.15)
        self.assertEqual(relation, "PO")

    def test_spatial_bind_non_tangential_proper_part(self):
        relation = self.evaluator.enforce_spatial_bind(5.0, 10.0)
        self.assertEqual(relation, "NTPP")

    def test_dccd_schema_guard_valid_f1(self):
        draft_output = {"word_count": 250}
        self.assertTrue(self.evaluator.enforce_dccd_schema_guard(
            draft_output, "F1_Executive_Summary"))

    def test_dccd_schema_guard_invalid_f1(self):
        draft_output = {"word_count": 100}
        self.assertFalse(self.evaluator.enforce_dccd_schema_guard(
            draft_output, "F1_Executive_Summary"))

    def test_dccd_schema_guard_valid_f3(self):
        draft_output = {"concept_count": 4}
        self.assertTrue(self.evaluator.enforce_dccd_schema_guard(
            draft_output, "F3_Emergent_Concepts"))

    def test_dccd_schema_guard_invalid_f3(self):
        draft_output = {"concept_count": 10}
        self.assertFalse(self.evaluator.enforce_dccd_schema_guard(
            draft_output, "F3_Emergent_Concepts"))

    def test_dccd_schema_guard_unknown_feature(self):
        draft_output = {"word_count": 250}
        self.assertFalse(self.evaluator.enforce_dccd_schema_guard(
            draft_output, "F99_Unknown"))

    def test_calculate_crs_perfect(self):
        crs = self.evaluator.calculate_crs(2, 2)
        self.assertEqual(crs, 1.0)

    def test_calculate_crs_failed(self):
        crs = self.evaluator.calculate_crs(1, 2)
        self.assertEqual(crs, 0.5)

    def test_calculate_crs_zero_div(self):
        crs = self.evaluator.calculate_crs(0, 0)
        self.assertEqual(crs, 1.0)

    def test_calculate_cfdi_zero_variance(self):
        cfdi = self.evaluator.calculate_cfdi(0.5, 0.5)
        self.assertEqual(cfdi, 0.0)

    def test_calculate_cfdi_with_nan(self):
        cfdi = self.evaluator.calculate_cfdi(float('nan'), 0.5)
        self.assertEqual(cfdi, 1.0)

    def test_epistemic_collision_protocol_pass(self):
        directives = ["A", "B"]
        actions = ["A", "B"]
        crs, cfdi, escrow = \
            self.evaluator.execute_epistemic_collision_protocol(
                directives, actions, 0.0001, 0.0001000005
            )
        self.assertEqual(crs, 1.0)
        self.assertTrue(cfdi <= 1e-6)
        self.assertFalse(escrow)
        self.assertEqual(len(self.evaluator.scar_registry), 0)

    def test_epistemic_collision_protocol_fail_crs(self):
        directives = ["A", "B", "C", "D", "E"]
        actions = ["A", "B", "C", "D"]  # 4/5 = 0.8 < 0.95
        crs, cfdi, escrow = \
            self.evaluator.execute_epistemic_collision_protocol(
                directives, actions, 0.0001, 0.0001
            )
        self.assertEqual(crs, 0.8)
        self.assertTrue(escrow)
        self.assertEqual(len(self.evaluator.scar_registry), 1)

    def test_epistemic_collision_protocol_fail_cfdi(self):
        directives = ["A", "B"]
        actions = ["A", "B"]
        crs, cfdi, escrow = \
            self.evaluator.execute_epistemic_collision_protocol(
                directives, actions, 0.0001, 0.0002
            )
        self.assertTrue(cfdi > 1e-6)
        self.assertTrue(escrow)
        self.assertEqual(len(self.evaluator.scar_registry), 1)

    def test_autonymic_isolate_valid(self):
        self.assertTrue(self.evaluator.check_autonymic_isolate("this is a normal draft text"))

    def test_autonymic_isolate_forbidden(self):
        self.assertFalse(self.evaluator.check_autonymic_isolate("this text contains hallucinated_syntax inside"))

    def test_mereology_route_valid(self):
        self.assertTrue(self.evaluator.enforce_mereology_route("Geometry-Physics", transitive_check=True))

    def test_mereology_route_invalid(self):
        self.assertFalse(self.evaluator.enforce_mereology_route("Invalid-Relation"))

    def test_topological_derivative(self):
        force = self.evaluator.calculate_topological_derivative(10.0, 2.0)
        self.assertEqual(force, 10.0 * (1.618 / 2.0))

    def test_topological_derivative_zero_bound(self):
        force = self.evaluator.calculate_topological_derivative(10.0, 0.0)
        self.assertEqual(force, float('inf'))

    def test_epsilon_tolerance_technical_debt_transition_fit(self):
        status = self.evaluator.evaluate_epsilon_tolerance_technical_debt(1.02, epsilon=0.05)
        self.assertEqual(status, "Transition Fit")

    def test_epsilon_tolerance_technical_debt_structural_failure(self):
        status = self.evaluator.evaluate_epsilon_tolerance_technical_debt(1.1, epsilon=0.05)
        self.assertEqual(status, "Structural Failure")

if __name__ == '__main__':
    unittest.main()
