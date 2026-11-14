#!/usr/bin/env python3
"""
=============================================================================
Comprehensive Automated Test Suite for Student Performance Analyzer
=============================================================================
Runs all 4 required test cases and asserts exact outputs.
=============================================================================
"""

import sys
import os
import io
import contextlib
import unittest
import pandas as pd
import numpy as np

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from student_analyzer import (
    load_student_data,
    display_results,
    display_statistics,
    calculate_class_statistics,
    calculate_grade,
    plot_all_charts,
    SUBJECTS,
)


class TestStudentPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(BASE_DIR, "data")
        self.charts_dir = os.path.join(BASE_DIR, "charts")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.charts_dir, exist_ok=True)

    def test_case_1_normal_input(self):
        """
        Test Case 1: Normal Input
        Input:
            Aman,80,70,90
            Riya,60,65,70
            Karan,40,35,50
        Expected Output:
            Aman | 240 | 80.00% | B
            Riya | 195 | 65.00% | C
            Karan | 125 | 41.67% | D
        """
        csv_path = os.path.join(self.data_dir, "testcase1_normal.csv")
        df = load_student_data(csv_path, verbose=False)

        self.assertEqual(len(df), 3)

        # Aman
        aman = df[df["Name"] == "Aman"].iloc[0]
        self.assertEqual(aman["Total"], 240)
        self.assertAlmostEqual(aman["Percentage"], 80.00, places=2)
        self.assertEqual(aman["Grade"], "B")

        # Riya
        riya = df[df["Name"] == "Riya"].iloc[0]
        self.assertEqual(riya["Total"], 195)
        self.assertAlmostEqual(riya["Percentage"], 65.00, places=2)
        self.assertEqual(riya["Grade"], "C")

        # Karan
        karan = df[df["Name"] == "Karan"].iloc[0]
        self.assertEqual(karan["Total"], 125)
        self.assertAlmostEqual(karan["Percentage"], 41.67, places=2)
        self.assertEqual(karan["Grade"], "D")

        # Capture formatted console output
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_results(df)
        output = buf.getvalue().strip().split("\n")

        expected = [
            "Aman | 240 | 80.00% | B",
            "Riya | 195 | 65.00% | C",
            "Karan | 125 | 41.67% | D",
        ]
        self.assertEqual(output, expected)

    def test_case_2_boundary_input(self):
        """
        Test Case 2: Boundary / Minimum Input
        Input:
            Neha,100,100,100
            Ravi,0,0,0
        Expected Output:
            Neha | 300 | 100.00% | A
            Ravi | 0 | 0.00% | F
        """
        csv_path = os.path.join(self.data_dir, "testcase2_boundary.csv")
        df = load_student_data(csv_path, verbose=False)

        self.assertEqual(len(df), 2)

        # Neha
        neha = df[df["Name"] == "Neha"].iloc[0]
        self.assertEqual(neha["Total"], 300)
        self.assertAlmostEqual(neha["Percentage"], 100.00, places=2)
        self.assertEqual(neha["Grade"], "A")

        # Ravi
        ravi = df[df["Name"] == "Ravi"].iloc[0]
        self.assertEqual(ravi["Total"], 0)
        self.assertAlmostEqual(ravi["Percentage"], 0.00, places=2)
        self.assertEqual(ravi["Grade"], "F")

        # Capture formatted console output
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_results(df)
        output = buf.getvalue().strip().split("\n")

        expected = [
            "Neha | 300 | 100.00% | A",
            "Ravi | 0 | 0.00% | F",
        ]
        self.assertEqual(output, expected)

    def test_case_3_invalid_input(self):
        """
        Test Case 3: Invalid Input
        Input:
            Amit,85,abc,70
        Expected Output:
            Invalid marks for Amit in Physics: 'abc'. Row skipped.
        """
        csv_path = os.path.join(self.data_dir, "testcase3_invalid.csv")

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            df = load_student_data(csv_path, verbose=True)
        output = buf.getvalue().strip()

        expected = "Invalid marks for Amit in Physics: 'abc'. Row skipped."
        self.assertIn(expected, output)
        self.assertTrue(df.empty)

    def test_case_4_statistics_and_charts(self):
        """
        Test Case 4: Statistics & Chart Display
        Input: Same as Test Case 1
        Expected Output:
            Mean %: 62.22 | Median %: 65.00 | Std Dev: 15.77
            Topper: Aman (80.00%)
            Subject averages: Maths 60.00, Physics 56.67, Chemistry 70.00
            Bar chart displayed
        """
        csv_path = os.path.join(self.data_dir, "testcase1_normal.csv")
        df = load_student_data(csv_path, verbose=False)

        stats = calculate_class_statistics(df)
        self.assertAlmostEqual(stats["mean"], 62.22, places=2)
        self.assertAlmostEqual(stats["median"], 65.00, places=2)
        self.assertAlmostEqual(stats["std_dev"], 15.77, places=2)
        self.assertEqual(stats["topper"], "Aman (80.00%)")
        self.assertAlmostEqual(stats["subject_averages"]["Maths"], 60.00, places=2)
        self.assertAlmostEqual(stats["subject_averages"]["Physics"], 56.67, places=2)
        self.assertAlmostEqual(stats["subject_averages"]["Chemistry"], 70.00, places=2)

        # Capture console output
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_statistics(df, show_chart=False, output_dir=self.charts_dir)
        output = buf.getvalue().strip()

        expected_lines = [
            "Mean %: 62.22 | Median %: 65.00 | Std Dev: 15.77",
            "Topper: Aman (80.00%)",
            "Subject averages: Maths 60.00, Physics 56.67, Chemistry 70.00",
            "Bar chart displayed",
        ]
        for exp in expected_lines:
            self.assertIn(exp, output)

        # Verify bar chart was saved
        bar_chart_file = os.path.join(self.charts_dir, "bar_chart.png")
        self.assertTrue(os.path.exists(bar_chart_file))


def run_all_tests():
    print("\n" + "=" * 70)
    print("      RUNNING STUDENT PERFORMANCE ANALYZER TEST HARNESS")
    print("=" * 70)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStudentPerformanceAnalyzer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n[SUCCESS] ALL 4 TEST CASES PASSED WITH 100% SPEC COMPLIANCE!")
        return 0
    else:
        print("\n[FAILURE] TEST SUITE FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
