# Student Performance Analyzer

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557c.svg)](https://matplotlib.org/)
[![Test Status](https://img.shields.io/badge/Tests-4%2F4%20Passing-brightgreen.svg)]()

A robust, console-driven Python 3 application designed to parse student academic marks across multiple subjects (**Maths, Physics, Chemistry**), calculate total scores, percentages, and letter grades, compute class-level descriptive statistics using **NumPy** and **Pandas**, and render insightful data visualizations (**Bar Charts** and **Histograms**) using **Matplotlib**.

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Key Concepts & Libraries](#key-concepts--libraries)
3. [Grade Evaluation Rubric](#grade-evaluation-rubric)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
   - [Interactive Console Mode](#interactive-console-mode)
   - [Command-Line Interface (CLI) Mode](#command-line-interface-cli-mode)
7. [Test Cases & Expected Outputs](#test-cases--expected-outputs)
8. [Visualizations](#visualizations)
9. [Automated Testing & Verification](#automated-testing--verification)
10. [Submission & GitHub Instructions](#submission--github-instructions)

---

## Problem Statement

Educational institutions require automated systems to evaluate and monitor student academic performance across cohorts. The **Student Performance Analyzer** addresses this by:
- Loading and sanitizing student performance records from CSV files.
- Computing individual student totals (out of 300) and percentages.
- Assigning standardized letter grades based on defined cutoff boundaries.
- Calculating central tendency and dispersion metrics: **Mean**, **Median**, and **Population Standard Deviation**.
- Identifying the class **Topper** and calculating individual **Subject-wise Averages**.
- Presenting visual charts including **Subject Average Bar Charts** and **Grade Distribution Histograms**.

---

## Key Concepts & Libraries

- **Pandas**: Used for DataFrame structured storage, row filtering, vectorized total calculations, and CSV parsing.
- **NumPy**: Used for high-performance numerical statistics (`np.mean`, `np.median`, `np.std(ddof=0)`).
- **Matplotlib**: Used for creating publication-quality charts (bar charts and histograms with annotations).
- **Statistics & Exception Handling**: Validates input formats, detects non-numeric marks or out-of-bound scores, logs detailed warnings, and skips malformed records gracefully.

---

## Grade Evaluation Rubric

Marks in each subject (**Maths, Physics, Chemistry**) are scored out of **100**. Total maximum marks across the 3 subjects is **300**.

| Percentage Range | Assigned Grade | Performance Category |
| :---: | :---: | :---: |
| **&ge; 90.00%** | **A** | Excellent |
| **&ge; 75.00% and < 90.00%** | **B** | Very Good |
| **&ge; 60.00% and < 75.00%** | **C** | Good |
| **&ge; 40.00% and < 60.00%** | **D** | Pass |
| **< 40.00%** | **F** | Fail |

$$\text{Total} = \text{Maths} + \text{Physics} + \text{Chemistry}$$
$$\text{Percentage} = \left(\frac{\text{Total}}{300}\right) \times 100$$

---

## Project Structure

```text
student_performance_analyzer/
├── student_analyzer.py          # Primary solution file containing core logic, CLI, and menu
├── run_tests.py                 # Comprehensive automated test harness (unittest)
├── generate_test_screenshots.py # High-res screenshot generator using Playwright / Edge
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation & execution guide
├── summary.md                   # Comprehensive summary report with embedded test screenshots
├── students.csv                 # Default input dataset
├── data/                        # Test case datasets
│   ├── testcase1_normal.csv     # Normal input scenario
│   ├── testcase2_boundary.csv   # Boundary limit scenario (100% and 0%)
│   ├── testcase3_invalid.csv    # Corrupted / invalid input scenario
│   ├── testcase4_stats.csv      # Statistical verification dataset
│   └── sample_students.csv      # Extended 20-student sample cohort
├── charts/                      # Generated Matplotlib charts
│   ├── bar_chart.png            # Subject-wise average bar chart
│   ├── histogram.png            # Percentage distribution histogram
│   └── student_performance_charts.png # Combined dashboard
└── screenshots/                 # High-resolution test run screenshots
    ├── test_case_1.png          # Normal input verification screenshot
    ├── test_case_2.png          # Boundary input verification screenshot
    ├── test_case_3.png          # Invalid input verification screenshot
    ├── test_case_4.png          # Class statistics & bar chart screenshot
    ├── test_suite_summary.png   # Full test harness pass summary
    └── interactive_menu.png     # Interactive console session screenshot
```

---

## Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your system.
- `pip` package manager.

### 1. Clone or Open the Repository
```bash
git clone https://github.com/<your-username>/student_performance_analyzer.git
cd student_performance_analyzer
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```
*(Core requirements: `pandas`, `numpy`, `matplotlib`. Optional for test screenshots: `playwright`, `pillow`)*

---

## Usage Guide

### Interactive Console Mode

Run `student_analyzer.py` directly without arguments to launch the interactive console menu:

```bash
python student_analyzer.py
```

```text
============================================================
      STUDENT PERFORMANCE ANALYZER (PYTHON 3)
============================================================

----------------------------------------
                  MAIN MENU
----------------------------------------
1. View Student Results (Total, %, Grade)
2. View Class Statistics & Display Bar Chart
3. Plot & Save All Charts (Bar Chart & Histogram)
4. Load Another CSV Dataset
5. Exit
----------------------------------------
Select an option (1-5):
```

### Command-Line Interface (CLI) Mode

You can also run specific options directly from the command line:

```bash
# 1. Display Student Results for default students.csv
python student_analyzer.py --option 1

# 2. Display Results for a specific CSV file
python student_analyzer.py --file data/testcase1_normal.csv --option 1

# 3. Display Class Statistics and show Bar Chart
python student_analyzer.py --file data/testcase1_normal.csv --option 2

# 4. Generate and save all charts without opening GUI windows
python student_analyzer.py --file data/sample_students.csv --save-charts --no-gui
```

---

## Test Cases & Expected Outputs

### Test Case 1: Normal Input
- **Dataset (`data/testcase1_normal.csv`)**:
  ```csv
  Aman,80,70,90
  Riya,60,65,70
  Karan,40,35,50
  ```
- **Execution**: `python student_analyzer.py --file data/testcase1_normal.csv --option 1`
- **Output**:
  ```text
  Aman | 240 | 80.00% | B
  Riya | 195 | 65.00% | C
  Karan | 125 | 41.67% | D
  ```

---

### Test Case 2: Boundary / Minimum Input
- **Dataset (`data/testcase2_boundary.csv`)**:
  ```csv
  Neha,100,100,100
  Ravi,0,0,0
  ```
- **Execution**: `python student_analyzer.py --file data/testcase2_boundary.csv --option 1`
- **Output**:
  ```text
  Neha | 300 | 100.00% | A
  Ravi | 0 | 0.00% | F
  ```

---

### Test Case 3: Invalid Input Handling
- **Dataset (`data/testcase3_invalid.csv`)**:
  ```csv
  Amit,85,abc,70
  ```
- **Execution**: File loading / verification
- **Output**:
  ```text
  Invalid marks for Amit in Physics: 'abc'. Row skipped.
  ```

---

### Test Case 4: Statistical Analysis & Visualization
- **Dataset**: Same CSV as Test Case 1 (`Aman,80,70,90`, `Riya,60,65,70`, `Karan,40,35,50`)
- **Execution**: `python student_analyzer.py --file data/testcase1_normal.csv --option 2`
- **Output**:
  ```text
  Mean %: 62.22 | Median %: 65.00 | Std Dev: 15.77
  Topper: Aman (80.00%)
  Subject averages: Maths 60.00, Physics 56.67, Chemistry 70.00
  Bar chart displayed
  ```

---

## Visualizations

The application automatically generates:
1. **Subject-Wise Averages Bar Chart** (`charts/bar_chart.png`): Compares class average performance across Maths, Physics, and Chemistry against the overall class mean.
2. **Grade Band Histogram** (`charts/histogram.png`): Illustrates the frequency distribution of student percentages across letter grade intervals ($F < 40$, $D \in [40, 60)$, $C \in [60, 75)$, $B \in [75, 90)$, $A \ge 90$).
3. **Comprehensive Performance Dashboard** (`charts/student_performance_charts.png`): Side-by-side analytical presentation.

---

## Automated Testing & Verification

Run the automated test harness:

```bash
python run_tests.py
```

Expected output:
```text
======================================================================
      RUNNING STUDENT PERFORMANCE ANALYZER TEST HARNESS
======================================================================
test_case_1_normal_input (__main__.TestStudentPerformanceAnalyzer.test_case_1_normal_input)
Test Case 1: Normal Input ... ok
test_case_2_boundary_input (__main__.TestStudentPerformanceAnalyzer.test_case_2_boundary_input)
Test Case 2: Boundary / Minimum Input ... ok
test_case_3_invalid_input (__main__.TestStudentPerformanceAnalyzer.test_case_3_invalid_input)
Test Case 3: Invalid Input ... ok
test_case_4_statistics_and_charts (__main__.TestStudentPerformanceAnalyzer.test_case_4_statistics_and_charts)
Test Case 4: Statistics & Chart Display ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.368s

OK

[SUCCESS] ALL 4 TEST CASES PASSED WITH 100% SPEC COMPLIANCE!
```

To re-generate the visual screenshot cards embedded in `summary.md`:
```bash
python generate_test_screenshots.py
```

---

## Submission & GitHub Instructions

To submit this project to GitHub:

```bash
# 1. Initialize git repository (if not already done)
git init

# 2. Add all project files
git add .

# 3. Create initial commit
git commit -m "feat: complete student performance analyzer with tests, charts, and summary report"

# 4. Link your remote repository and push
git remote add origin https://github.com/<your-username>/student-performance-analyzer.git
git branch -M main
git push -u origin main
```
