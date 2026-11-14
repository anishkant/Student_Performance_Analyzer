# Project: Student Performance Analyzer
# Concepts: Pandas, NumPy, Matplotlib, Statistics

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SUBJECTS = ["Maths", "Physics", "Chemistry"]


def calculate_grade(percentage):
    """Assign letter grade based on percentage."""
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def load_student_data(filepath="students.csv"):
    """Load and validate student records from CSV."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return pd.DataFrame()

    valid_rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("Warning: CSV file is empty.")
        return pd.DataFrame()

    # Check if first line is a header
    first_tokens = [t.strip() for t in lines[0].split(",")]
    header_names = ["name", "student", "student_name", "student name", "roll", "id"]
    has_header = False
    if first_tokens and first_tokens[0].lower() in header_names:
        has_header = True

    start_idx = 1 if has_header else 0

    for line in lines[start_idx:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue

        name = parts[0]
        row_valid = True
        marks = []

        for i, sub in enumerate(SUBJECTS):
            val_str = parts[i + 1]
            try:
                val = float(val_str)
                if val < 0 or val > 100:
                    print(f"Invalid marks for {name} in {sub}: '{val_str}'. Row skipped.")
                    row_valid = False
                    break
                marks.append(val)
            except ValueError:
                print(f"Invalid marks for {name} in {sub}: '{val_str}'. Row skipped.")
                row_valid = False
                break

        if row_valid:
            valid_rows.append([name, marks[0], marks[1], marks[2]])

    df = pd.DataFrame(valid_rows, columns=["Name", "Maths", "Physics", "Chemistry"])
    if not df.empty:
        df["Total"] = df[SUBJECTS].sum(axis=1)
        df["Percentage"] = (df["Total"] / 300.0) * 100.0
        df["Grade"] = df["Percentage"].apply(calculate_grade)

    return df


def display_results(df):
    """Option 1: Display totals, percentages and grades."""
    if df.empty:
        print("No student records available.")
        return

    for _, row in df.iterrows():
        total_str = int(row["Total"]) if row["Total"].is_integer() else f"{row['Total']:.2f}"
        print(f"{row['Name']} | {total_str} | {row['Percentage']:.2f}% | {row['Grade']}")


def display_statistics(df):
    """Option 2: Calculate and display statistics, then show bar chart."""
    if df.empty:
        print("No student records available for statistics.")
        return

    percentages = df["Percentage"].values
    mean_val = np.mean(percentages)
    median_val = np.median(percentages)
    std_val = np.std(percentages, ddof=0)

    # Topper
    max_pct = df["Percentage"].max()
    toppers = df[df["Percentage"] == max_pct]["Name"].tolist()
    topper_str = f"{', '.join(toppers)} ({max_pct:.2f}%)"

    # Subject averages
    maths_avg = df["Maths"].mean()
    phys_avg = df["Physics"].mean()
    chem_avg = df["Chemistry"].mean()

    print(f"Mean %: {mean_val:.2f} | Median %: {median_val:.2f} | Std Dev: {std_val:.2f}")
    print(f"Topper: {topper_str}")
    print(f"Subject averages: Maths {maths_avg:.2f}, Physics {phys_avg:.2f}, Chemistry {chem_avg:.2f}")

    # Plot bar chart
    plot_bar_chart(df)
    print("Bar chart displayed")


def plot_bar_chart(df):
    """Plot bar chart for subject averages."""
    if df.empty:
        return

    subjects = ["Maths", "Physics", "Chemistry"]
    averages = [df["Maths"].mean(), df["Physics"].mean(), df["Chemistry"].mean()]

    plt.figure(figsize=(7, 4.5))
    bars = plt.bar(subjects, averages, color=["#4A90E2", "#50E3C2", "#F5A623"], width=0.5, edgecolor="black")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f"{height:.2f}", ha="center", va="bottom", fontsize=10)

    plt.ylim(0, 105)
    plt.title("Subject-Wise Class Averages")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks (out of 100)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    plt.savefig("bar_chart.png")
    try:
        plt.show(block=False)
        plt.pause(1.5)
        plt.close()
    except Exception:
        pass


def plot_histogram(df):
    """Plot histogram for student percentage distribution."""
    if df.empty:
        return

    plt.figure(figsize=(7, 4.5))
    bins = [0, 40, 60, 75, 90, 100]
    plt.hist(df["Percentage"], bins=bins, color="#7B68EE", edgecolor="black", rwidth=0.85)

    plt.title("Student Percentage Distribution")
    plt.xlabel("Percentage Ranges")
    plt.ylabel("Number of Students")
    plt.xticks(bins, ["0 (F)", "40 (D)", "60 (C)", "75 (B)", "90 (A)", "100"])
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    plt.savefig("histogram.png")
    try:
        plt.show(block=False)
        plt.pause(1.5)
        plt.close()
    except Exception:
        pass


def main():
    current_file = sys.argv[1] if len(sys.argv) > 1 else "students.csv"

    if not os.path.exists(current_file):
        current_file = input("Enter path to student CSV file: ").strip()

    df = load_student_data(current_file)

    while True:
        print("\n" + "=" * 40)
        print("     STUDENT PERFORMANCE ANALYZER")
        print("=" * 40)
        print("1. View Student Results")
        print("2. View Class Statistics & Bar Chart")
        print("3. View Percentage Distribution (Histogram)")
        print("4. Load Another CSV File")
        print("5. Exit")
        print("-" * 40)

        choice = input("Enter choice (1-5): ").replace("\ufeff", "").strip()

        if choice == "1":
            print("\n--- Student Results ---")
            display_results(df)
        elif choice == "2":
            print("\n--- Class Statistics ---")
            display_statistics(df)
        elif choice == "3":
            print("\n--- Plotting Histogram ---")
            plot_histogram(df)
            print("Histogram displayed")
        elif choice == "4":
            new_file = input("Enter new CSV file path: ").strip()
            if os.path.exists(new_file):
                current_file = new_file
                df = load_student_data(current_file)
                print(f"Loaded '{current_file}' successfully.")
            else:
                print(f"Error: File '{new_file}' does not exist.")
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid input, please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
