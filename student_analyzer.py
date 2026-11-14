#!/usr/bin/env python3
"""
=============================================================================
Student Performance Analyzer
=============================================================================
Problem Statement:
    Analyse student marks across subjects from a dataset to calculate totals,
    percentages, grades, and class statistics, and present the results with charts.

Language: Python 3
Concepts: Pandas, NumPy, Matplotlib, Statistics
Subjects: Maths, Physics, Chemistry (Marks out of 100 each, Total: 300)
Grades:
    >= 90 : A
    >= 75 : B
    >= 60 : C
    >= 40 : D
    < 40  : F
=============================================================================
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Default subjects
SUBJECTS = ["Maths", "Physics", "Chemistry"]
MAX_MARKS_PER_SUBJECT = 100.0
TOTAL_MAX_MARKS = len(SUBJECTS) * MAX_MARKS_PER_SUBJECT

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CHARTS_DIR = os.path.join(BASE_DIR, "charts")


def calculate_grade(percentage: float) -> str:
    """Assign letter grade based on percentage."""
    if percentage >= 90.0:
        return "A"
    elif percentage >= 75.0:
        return "B"
    elif percentage >= 60.0:
        return "C"
    elif percentage >= 40.0:
        return "D"
    else:
        return "F"


def load_student_data(filepath: str, verbose: bool = True) -> pd.DataFrame:
    """
    Load student data from CSV file with robust validation.
    Handles files with or without headers. Skips and reports invalid rows.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found: {filepath}")

    valid_rows = []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        if verbose:
            print(f"Warning: '{filepath}' is empty.")
        return pd.DataFrame(columns=["Name"] + SUBJECTS)

    # Check if first line is a header
    first_tokens = [t.strip() for t in lines[0].split(",")]
    header_identifiers = {"name", "student", "student_name", "student name", "roll", "roll_no", "roll no", "id"}
    has_header = False
    if first_tokens:
        if first_tokens[0].lower() in header_identifiers:
            has_header = True
        elif all(not t.replace(".", "", 1).isdigit() for t in first_tokens):
            has_header = True

    start_idx = 1 if has_header else 0

    for line_num, line in enumerate(lines[start_idx:], start=start_idx + 1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            if verbose:
                print(f"Malformed row skipped on line {line_num}: '{line}'")
            continue

        name = parts[0]
        row_valid = True
        marks = []

        for i, sub in enumerate(SUBJECTS):
            raw_val = parts[i + 1]
            try:
                val = float(raw_val)
                if val < 0 or val > 100:
                    if verbose:
                        print(f"Invalid marks for {name} in {sub}: '{raw_val}'. Row skipped.")
                    row_valid = False
                    break
                marks.append(val)
            except ValueError:
                if verbose:
                    print(f"Invalid marks for {name} in {sub}: '{raw_val}'. Row skipped.")
                row_valid = False
                break

        if row_valid:
            valid_rows.append([name, marks[0], marks[1], marks[2]])

    columns = ["Name", "Maths", "Physics", "Chemistry"]
    df = pd.DataFrame(valid_rows, columns=columns)

    if not df.empty:
        # Calculate Total, Percentage, and Grade
        df["Total"] = df[SUBJECTS].sum(axis=1)
        df["Percentage"] = (df["Total"] / TOTAL_MAX_MARKS) * 100.0
        df["Grade"] = df["Percentage"].apply(calculate_grade)

    return df


def display_results(df: pd.DataFrame) -> None:
    """
    Menu Option 1: Display student results (Name | Total | Percentage% | Grade).
    """
    if df.empty:
        print("No valid student records to display.")
        return

    for _, row in df.iterrows():
        total_val = int(row["Total"]) if row["Total"].is_integer() else f"{row['Total']:.2f}"
        print(f"{row['Name']} | {total_val} | {row['Percentage']:.2f}% | {row['Grade']}")


def calculate_class_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate mean, median, population standard deviation, topper, and subject averages.
    """
    if df.empty:
        return {}

    percentages = df["Percentage"].values

    mean_pct = float(np.mean(percentages))
    median_pct = float(np.median(percentages))
    # Standard deviation: population std dev (ddof=0)
    std_dev_pct = float(np.std(percentages, ddof=0))

    # Topper (highest percentage)
    max_pct = df["Percentage"].max()
    toppers = df[df["Percentage"] == max_pct]
    topper_names = ", ".join(toppers["Name"].tolist())
    topper_info = f"{topper_names} ({max_pct:.2f}%)"

    # Subject averages
    subject_avgs = {sub: float(df[sub].mean()) for sub in SUBJECTS}

    return {
        "mean": mean_pct,
        "median": median_pct,
        "std_dev": std_dev_pct,
        "topper": topper_info,
        "subject_averages": subject_avgs,
        "total_students": len(df),
    }


def display_statistics(df: pd.DataFrame, show_chart: bool = True, output_dir: str = None) -> None:
    """
    Menu Option 2: Display class statistics and trigger bar chart display.
    """
    if output_dir is None:
        output_dir = DEFAULT_CHARTS_DIR

    if df.empty:
        print("No valid student records available for statistics.")
        return

    stats = calculate_class_statistics(df)

    print(f"Mean %: {stats['mean']:.2f} | Median %: {stats['median']:.2f} | Std Dev: {stats['std_dev']:.2f}")
    print(f"Topper: {stats['topper']}")

    sub_avgs = stats["subject_averages"]
    sub_str = f"Maths {sub_avgs['Maths']:.2f}, Physics {sub_avgs['Physics']:.2f}, Chemistry {sub_avgs['Chemistry']:.2f}"
    print(f"Subject averages: {sub_str}")

    # Generate and display/save Bar Chart
    os.makedirs(output_dir, exist_ok=True)
    bar_chart_path = os.path.join(output_dir, "bar_chart.png")
    plot_bar_chart(df, save_path=bar_chart_path, show=show_chart)
    print("Bar chart displayed")


def plot_bar_chart(df: pd.DataFrame, save_path: str = None, show: bool = True) -> None:
    """
    Plot high-clarity bar chart showing subject averages and individual student performance.
    """
    if df.empty:
        return

    stats = calculate_class_statistics(df)
    sub_avgs = stats["subject_averages"]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

    subjects = list(sub_avgs.keys())
    averages = list(sub_avgs.values())
    colors = ["#3b82f6", "#10b981", "#f59e0b"]

    bars = ax.bar(subjects, averages, color=colors, width=0.5, edgecolor="#1e293b", linewidth=1.2)

    # Annotate bar values
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#1e293b",
        )

    ax.set_ylim(0, 110)
    ax.set_ylabel("Average Score / Marks", fontsize=12, fontweight="bold")
    ax.set_title("Subject-Wise Class Performance Averages", fontsize=14, fontweight="bold", pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Class Mean Reference Line
    class_mean = stats["mean"]
    ax.axhline(class_mean, color="#ef4444", linestyle="--", linewidth=1.5, label=f"Class Mean %: {class_mean:.2f}%")
    ax.legend(loc="upper right", frameon=True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    if show:
        try:
            plt.show(block=False)
            plt.pause(0.5)
        except Exception:
            pass
    plt.close(fig)


def plot_histogram(df: pd.DataFrame, save_path: str = None, show: bool = True) -> None:
    """
    Plot histogram showing distribution of student overall percentages.
    """
    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    percentages = df["Percentage"].values

    bins = [0, 40, 60, 75, 90, 100]
    n, bins_out, patches = ax.hist(
        percentages, bins=bins, edgecolor="#0f172a", linewidth=1.2, color="#6366f1", alpha=0.85, rwidth=0.9
    )

    # Color bins according to grade bands
    grade_colors = ["#ef4444", "#f97316", "#eab308", "#3b82f6", "#10b981"]
    for patch, color in zip(patches, grade_colors):
        patch.set_facecolor(color)

    ax.set_xlabel("Percentage Range (%)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Number of Students", fontsize=12, fontweight="bold")
    ax.set_title("Student Percentage Distribution by Grade Band", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(bins)
    ax.set_xticklabels(["0 (F)", "40 (D)", "60 (C)", "75 (B)", "90 (A)", "100"])
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Annotate counts
    for count, patch in zip(n, patches):
        if count > 0:
            ax.annotate(
                f"{int(count)}",
                xy=(patch.get_x() + patch.get_width() / 2, count),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
            )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    if show:
        try:
            plt.show(block=False)
            plt.pause(0.5)
        except Exception:
            pass
    plt.close(fig)


def plot_all_charts(df: pd.DataFrame, output_dir: str = None, show: bool = True) -> tuple:
    """
    Generate and save both the bar chart, histogram, and combined comprehensive dashboard.
    """
    if output_dir is None:
        output_dir = DEFAULT_CHARTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    bar_path = os.path.join(output_dir, "bar_chart.png")
    hist_path = os.path.join(output_dir, "histogram.png")
    combined_path = os.path.join(output_dir, "student_performance_charts.png")

    plot_bar_chart(df, save_path=bar_path, show=show)
    plot_histogram(df, save_path=hist_path, show=show)

    # Combined figure
    if not df.empty:
        stats = calculate_class_statistics(df)
        sub_avgs = stats["subject_averages"]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

        # 1. Bar Chart
        subjects = list(sub_avgs.keys())
        averages = list(sub_avgs.values())
        colors = ["#3b82f6", "#10b981", "#f59e0b"]
        bars = ax1.bar(subjects, averages, color=colors, width=0.45, edgecolor="#1e293b", linewidth=1.2)
        for bar in bars:
            h = bar.get_height()
            ax1.annotate(
                f"{h:.2f}%",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=10,
            )
        ax1.axhline(stats["mean"], color="#ef4444", linestyle="--", label=f"Class Mean: {stats['mean']:.2f}%")
        ax1.set_ylim(0, 110)
        ax1.set_title("Subject-Wise Averages", fontsize=13, fontweight="bold")
        ax1.set_ylabel("Average Marks (%)", fontsize=11, fontweight="bold")
        ax1.grid(axis="y", linestyle="--", alpha=0.4)
        ax1.legend(loc="upper right")

        # 2. Histogram
        bins = [0, 40, 60, 75, 90, 100]
        n, _, patches = ax2.hist(
            df["Percentage"].values, bins=bins, edgecolor="#0f172a", linewidth=1.2, rwidth=0.9
        )
        grade_colors = ["#ef4444", "#f97316", "#eab308", "#3b82f6", "#10b981"]
        for patch, color in zip(patches, grade_colors):
            patch.set_facecolor(color)
        ax2.set_title("Percentage Distribution & Grades", fontsize=13, fontweight="bold")
        ax2.set_xlabel("Percentage Range", fontsize=11, fontweight="bold")
        ax2.set_ylabel("Student Count", fontsize=11, fontweight="bold")
        ax2.set_xticks(bins)
        ax2.set_xticklabels(["0 (F)", "40 (D)", "60 (C)", "75 (B)", "90 (A)", "100"])
        ax2.grid(axis="y", linestyle="--", alpha=0.4)
        for count, patch in zip(n, patches):
            if count > 0:
                ax2.annotate(
                    f"{int(count)}",
                    xy=(patch.get_x() + patch.get_width() / 2, count),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

        fig.suptitle("Student Performance Analytics Dashboard", fontsize=16, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(combined_path, dpi=200, bbox_inches="tight")
        if show:
            try:
                plt.show(block=False)
                plt.pause(0.5)
            except Exception:
                pass
        plt.close(fig)

    return bar_path, hist_path, combined_path


def run_interactive_menu(filepath: str = "students.csv") -> None:
    """
    Console Menu System allowing interactive usage.
    """
    current_file = filepath

    print("\n" + "=" * 60)
    print("      STUDENT PERFORMANCE ANALYZER (PYTHON 3)")
    print("=" * 60)

    try:
        df = load_student_data(current_file, verbose=True)
    except Exception as e:
        print(f"Error loading {current_file}: {e}")
        df = pd.DataFrame()

    while True:
        print("\n" + "-" * 40)
        print("                  MAIN MENU")
        print("-" * 40)
        print("1. View Student Results (Total, %, Grade)")
        print("2. View Class Statistics & Display Bar Chart")
        print("3. Plot & Save All Charts (Bar Chart & Histogram)")
        print("4. Load Another CSV Dataset")
        print("5. Exit")
        print("-" * 40)

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            print("\n[STUDENT RESULTS]")
            display_results(df)
        elif choice == "2":
            print("\n[CLASS STATISTICS]")
            display_statistics(df, show_chart=True)
        elif choice == "3":
            print("\n[PLOTTING CHARTS]")
            b, h, c = plot_all_charts(df, output_dir=DEFAULT_CHARTS_DIR, show=True)
            print(f"Bar chart saved: {b}")
            print(f"Histogram saved: {h}")
            print(f"Combined dashboard saved: {c}")
        elif choice == "4":
            new_path = input("Enter path to new CSV file: ").strip()
            if os.path.exists(new_path):
                current_file = new_path
                df = load_student_data(current_file, verbose=True)
                print(f"Loaded '{current_file}' successfully with {len(df)} records.")
            else:
                print(f"Error: File '{new_path}' does not exist.")
        elif choice == "5":
            print("\nExiting Student Performance Analyzer. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")


def main():
    parser = argparse.ArgumentParser(description="Student Performance Analyzer")
    parser.add_argument("--file", "-f", default="students.csv", help="Path to student CSV file")
    parser.add_argument(
        "--option", "-o", type=int, choices=[1, 2, 3], help="Execute menu option directly (1=Results, 2=Stats, 3=Charts)"
    )
    parser.add_argument("--save-charts", action="store_true", help="Save charts to disk without interactive GUI")
    parser.add_argument("--no-gui", action="store_true", help="Run without opening GUI windows")

    args = parser.parse_args()

    if args.no_gui:
        matplotlib.use("Agg")

    if args.option is not None or args.save_charts:
        # Non-interactive CLI mode
        df = load_student_data(args.file, verbose=True)

        if args.option == 1:
            display_results(df)
        elif args.option == 2:
            display_statistics(df, show_chart=not args.no_gui)
        elif args.option == 3 or args.save_charts:
            plot_all_charts(df, output_dir=DEFAULT_CHARTS_DIR, show=not args.no_gui)
            print("Charts generated and saved successfully.")
    else:
        # Interactive console mode
        run_interactive_menu(args.file)


if __name__ == "__main__":
    main()
