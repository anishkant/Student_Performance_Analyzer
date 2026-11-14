# Student Performance Analyzer

A Python-based data analysis tool to analyze student marks across subjects (**Maths, Physics, Chemistry**), calculate total marks, percentages, letter grades, and class statistics, and visualize results using **Matplotlib** charts.

---

## Features
- **Data Ingestion**: Loads student records from CSV files with error handling for missing or invalid data.
- **Result Calculation**: Computes individual student totals (out of 300), percentages, and assigns letter grades (A, B, C, D, F).
- **Statistical Analysis**: Calculates class Mean %, Median %, Population Standard Deviation, topper(s), and subject-wise averages using **NumPy** and **Pandas**.
- **Data Visualization**: Generates subject average bar charts and grade distribution histograms using **Matplotlib**.
- **Interactive Console Menu**: Simple, interactive menu for running all features.

---

## Grading System
Each subject is scored out of 100 marks. Total marks are out of 300.

| Percentage | Grade |
| :--- | :---: |
| &ge; 90% | **A** |
| &ge; 75% | **B** |
| &ge; 60% | **C** |
| &ge; 40% | **D** |
| Below 40% | **F** |

---

## Project Structure
```text
student_performance_analyzer/
│
├── student_analyzer.py      # Main Python script (Console application)
├── students.csv             # Default input data file
├── requirements.txt         # Required Python packages
├── README.md                # Project documentation
├── summary.md               # Summary report with test case screenshots
│
├── data/                    # Test case CSV files
│   ├── testcase1_normal.csv
│   ├── testcase2_boundary.csv
│   ├── testcase3_invalid.csv
│   ├── testcase4_stats.csv
│   └── sample_students.csv
│
├── charts/                  # Generated charts
│   ├── bar_chart.png
│   └── histogram.png
│
└── screenshots/             # Screenshots of terminal outputs
    ├── test_case_1.png
    ├── test_case_2.png
    ├── test_case_3.png
    ├── test_case_4.png
    └── histogram_view.png
```

---

## Requirements & Installation

### Requirements
- Python 3.x
- `pandas`
- `numpy`
- `matplotlib`

### Installation
Install required packages using:
```bash
pip install -r requirements.txt
```

---

## How to Run

Run the main script from the terminal:
```bash
python student_analyzer.py
```

Or pass a specific CSV file:
```bash
python student_analyzer.py data/testcase1_normal.csv
```

### Main Menu Options:
```text
========================================
     STUDENT PERFORMANCE ANALYZER
========================================
1. View Student Results
2. View Class Statistics & Bar Chart
3. View Percentage Distribution (Histogram)
4. Load Another CSV File
5. Exit
----------------------------------------
Enter choice (1-5):
```

---

## Test Cases

### Test Case 1: Normal Input
- **Input (`data/testcase1_normal.csv`)**:
  ```csv
  Aman,80,70,90
  Riya,60,65,70
  Karan,40,35,50
  ```
- **Option 1 Output**:
  ```text
  Aman | 240 | 80.00% | B
  Riya | 195 | 65.00% | C
  Karan | 125 | 41.67% | D
  ```

### Test Case 2: Boundary / Minimum Input
- **Input (`data/testcase2_boundary.csv`)**:
  ```csv
  Neha,100,100,100
  Ravi,0,0,0
  ```
- **Option 1 Output**:
  ```text
  Neha | 300 | 100.00% | A
  Ravi | 0 | 0.00% | F
  ```

### Test Case 3: Invalid Input
- **Input (`data/testcase3_invalid.csv`)**:
  ```csv
  Amit,85,abc,70
  ```
- **Output**:
  ```text
  Invalid marks for Amit in Physics: 'abc'. Row skipped.
  ```

### Test Case 4: Statistics & Bar Chart
- **Input**: Same as Test Case 1
- **Option 2 Output**:
  ```text
  Mean %: 62.22 | Median %: 65.00 | Std Dev: 15.77
  Topper: Aman (80.00%)
  Subject averages: Maths 60.00, Physics 56.67, Chemistry 70.00
  Bar chart displayed
  ```

---

## GitHub Setup
To upload this project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit: Student Performance Analyzer"
git remote add origin https://github.com/<your-username>/student-performance-analyzer.git
git branch -M main
git push -u origin main
```
