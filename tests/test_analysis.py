"""Check data integrity decisions and independently verify grouped calculations."""
from pathlib import Path
import tempfile
import unittest
import numpy as np
import pandas as pd
from analysis import load_and_validate, bootstrap_mean, sql_summary, summarize_groups

ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    def test_original_dataset_integrity(self):
        data, audit = load_and_validate(ROOT / "data/raw/student-por.csv")
        self.assertEqual(len(data), 649)
        self.assertEqual(audit["missing_cells_source"], 0)
        self.assertEqual(audit["exact_duplicate_rows_source"], 0)
        self.assertEqual(audit["zero_final_grades"], 15)
        self.assertEqual(audit["rows_removed"], 0)

    def test_sql_and_group_statistics_against_hand_calculation(self):
        data = pd.DataFrame({"school": ["GP", "GP", "MS", "MS"],
                             "studytime": [1, 1, 2, 2], "absences": [0, 2, 4, 6],
                             "G3": [8, 12, 14, 18]})
        result = sql_summary(data)
        np.testing.assert_array_equal(result.n, [2, 2])
        np.testing.assert_allclose(result.mean_grade, [10, 16])
        np.testing.assert_allclose(result.mean_absences, [1, 5])
        grouped = summarize_groups(data, ["studytime"])
        np.testing.assert_allclose(grouped.mean_grade, [10, 16])
        self.assertEqual(sql_summary(data, "GP").n.sum(), 2)

    def test_parameterized_filter_does_not_interpret_sql(self):
        data, _ = load_and_validate(ROOT / "data/raw/student-por.csv")
        self.assertTrue(sql_summary(data, "GP' OR 1=1 --").empty)

    def test_bootstrap_known_constant_and_seed(self):
        self.assertEqual(bootstrap_mean([7]*10, np.random.default_rng(42)), (7, 7))
        a = bootstrap_mean([1, 4, 7, 10], np.random.default_rng(42))
        b = bootstrap_mean([1, 4, 7, 10], np.random.default_rng(42))
        self.assertEqual(a, b)
        self.assertLessEqual(a[0], a[1])

    def test_invalid_input_rejected(self):
        data = pd.DataFrame({"school": ["GP"], "studytime": [1], "absences": [0], "G1": [10], "G2": [11], "G3": [12]})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"invalid.csv"
            for column, value in [("G3", 21), ("studytime", 5), ("absences", -1), ("G1", 9.5), ("G2", np.nan)]:
                changed = data.astype({column: float}) if column != "school" else data.copy()
                changed.loc[0, column] = value
                changed.to_csv(path, sep=";", index=False)
                with self.assertRaises(ValueError):
                    load_and_validate(path)

    def test_matching_selected_profiles_are_preserved(self):
        data = pd.DataFrame({"school": ["GP", "GP"], "studytime": [1, 1], "absences": [0, 0],
                             "G1": [10, 10], "G2": [11, 11], "G3": [0, 0], "unused": ["a", "b"]})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"profiles.csv"
            data.to_csv(path, sep=";", index=False)
            result, audit = load_and_validate(path)
            self.assertEqual(len(result), 2)
            self.assertEqual(audit["identical_selected_profiles"], 1)
            self.assertEqual(audit["zero_final_grades"], 2)


if __name__ == "__main__":
    unittest.main()
