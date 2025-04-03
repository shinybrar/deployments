"""Enhanced visualization module for analyzing Kubernetes vs Kueue benchmark results."""

import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from matplotlib.ticker import ScalarFormatter

app = typer.Typer(help="Plot Benchmark Results")


def load_and_clean_results(filename: str) -> pd.DataFrame:
    """
    Load benchmark results from a CSV file and clean the data.

    Args:
        filename: Path to the CSV file

    Returns:
        DataFrame with cleaned benchmark results
    """
    if not os.path.isfile(filename):
        print(f"Error: Results file {filename} not found.")
        return pd.DataFrame()

    # Load data
    df = pd.read_csv(filename)

    if df.empty:
        print("Warning: No data found in results file.")
        return df

    # Convert boolean columns
    df["use_kueue"] = df["use_kueue"].astype(bool)

    # Convert datetime columns
    datetime_cols = [
        "first_creation_time",
        "last_creation_time",
        "first_completion_time",
        "last_completion_time",
    ]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Remove duplicate experiments by keeping only the latest timestamp for each
    # combination of job_count and use_kueue
    df = df.sort_values("timestamp").drop_duplicates(
        subset=["job_count", "use_kueue"], keep="last"
    )

    # Sort by job_count for easier analysis
    df = df.sort_values(["job_count", "use_kueue"])

    print(f"Loaded and cleaned {len(df)} experiment results from {filename}")
    return df


def plot_completion_times(  # noqa: C901
    df: pd.DataFrame,
    output_file: str = "completion_times.png",
    log_scale: bool = True,
    title: Optional[str] = None,
) -> None:
    """
    Plot job completion times for direct vs Kueue experiments.

    Args:
        df: DataFrame containing experiment results
        output_file: Path to save the plot
        log_scale: Whether to use log scale for x-axis
        title: Custom title for the plot
    """
    # Filter data for direct and kueue runs
    direct_df = df[~df["use_kueue"]]
    kueue_df = df[df["use_kueue"]]

    if direct_df.empty or kueue_df.empty:
        print("Warning: Insufficient data for plotting completion times.")
        return

    # Extract data for plotting
    direct_counts = direct_df["job_count"].values
    direct_times = direct_df["total_time_from_first_creation_to_last_completion"].values

    kueue_counts = kueue_df["job_count"].values
    kueue_times = kueue_df["total_time_from_first_creation_to_last_completion"].values

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot data points with lines
    plt.scatter(
        direct_counts,
        direct_times,
        color="blue",
        marker="o",
        s=80,
        label="Direct Kubernetes",
    )
    plt.plot(direct_counts, direct_times, "b-", linewidth=2)

    plt.scatter(
        kueue_counts, kueue_times, color="red", marker="x", s=80, label="With Kueue"
    )
    plt.plot(kueue_counts, kueue_times, "r-", linewidth=2)

    # Set log scale if requested
    if log_scale:
        plt.xscale("log", base=2)

    # Add gridlines
    plt.grid(True, linestyle="--", alpha=0.7)

    # Format axis labels
    plt.xlabel("Number of Jobs", fontsize=14)
    plt.ylabel("Completion Time (seconds)", fontsize=14)

    # Set plot title
    if title:
        plt.title(title, fontsize=16)
    else:
        plt.title("Job Completion Time: Direct Kubernetes vs Kueue", fontsize=16)

    # Add legend
    plt.legend(fontsize=12)

    # Format y-axis with comma separators
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())

    # Set x-ticks to match the tested job counts
    all_counts = sorted(set(direct_counts) | set(kueue_counts))
    plt.xticks(all_counts, [str(count) for count in all_counts], rotation=45)

    # Add value annotations
    for count, time in zip(direct_counts, direct_times, strict=False):
        plt.annotate(
            f"{time:.1f}s",
            (count, time),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    for count, time in zip(kueue_counts, kueue_times, strict=False):
        plt.annotate(
            f"{time:.1f}s",
            (count, time),
            textcoords="offset points",
            xytext=(0, -15),
            ha="center",
        )

    # Add trend lines with equations
    if len(direct_counts) > 1:
        if log_scale:
            x_values = np.log2(direct_counts)
        else:
            x_values = direct_counts

        direct_z = np.polyfit(x_values, direct_times, 1)
        direct_p = np.poly1d(direct_z)

        x_range = np.linspace(min(direct_counts), max(direct_counts), 100)
        if log_scale:
            y_values = direct_p(np.log2(x_range))
        else:
            y_values = direct_p(x_range)

        plt.plot(x_range, y_values, "b--", alpha=0.5)

        # Add trend equation
        equation_text = (
            f"y = {direct_z[0]:.2f}x + {direct_z[1]:.2f}"
            if not log_scale
            else f"y = {direct_z[0]:.2f}log₂(x) + {direct_z[1]:.2f}"
        )
        plt.annotate(
            f"Direct trend: {equation_text}",
            xy=(0.05, 0.95),
            xycoords="axes fraction",
            bbox={
                "boxstyle": "round,pad=0.3",
                "fc": "white",
                "ec": "blue",
                "alpha": 0.8,
            },
        )

    if len(kueue_counts) > 1:
        if log_scale:
            x_values = np.log2(kueue_counts)
        else:
            x_values = kueue_counts

        kueue_z = np.polyfit(x_values, kueue_times, 1)
        kueue_p = np.poly1d(kueue_z)

        x_range = np.linspace(min(kueue_counts), max(kueue_counts), 100)
        if log_scale:
            y_values = kueue_p(np.log2(x_range))
        else:
            y_values = kueue_p(x_range)

        plt.plot(x_range, y_values, "r--", alpha=0.5)

        # Add trend equation
        equation_text = (
            f"y = {kueue_z[0]:.2f}x + {kueue_z[1]:.2f}"
            if not log_scale
            else f"y = {kueue_z[0]:.2f}log₂(x) + {kueue_z[1]:.2f}"
        )
        plt.annotate(
            f"Kueue trend: {equation_text}",
            xy=(0.05, 0.89),
            xycoords="axes fraction",
            bbox={
                "boxstyle": "round,pad=0.3",
                "fc": "white",
                "ec": "red",
                "alpha": 0.8,
            },
        )

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Completion time plot saved to {output_file}")


def plot_performance_comparison(
    df: pd.DataFrame,
    output_file: str = "performance_comparison.png",
    metric: str = "total_time_from_first_creation_to_last_completion",
) -> None:
    """
    Plot performance comparison between direct and Kueue approaches.

    Args:
        df: DataFrame containing experiment results
        output_file: Path to save the plot
        metric: The performance metric to compare
    """
    # Create a pivot table to easily compare direct vs kueue for each job count
    pivot_df = df.pivot_table(
        index="job_count",
        columns="use_kueue",
        values=metric,
        aggfunc="mean",  # In case of duplicates
    ).reset_index()

    # Rename columns for clarity
    pivot_df.columns.name = None
    pivot_df = pivot_df.rename(columns={False: "direct", True: "kueue"})

    # Filter to include only complete pairs and sort
    pivot_df = pivot_df.dropna().sort_values("job_count")

    if len(pivot_df) == 0:
        print("Warning: No complete pairs of direct/kueue data for comparison.")
        return

    # Calculate differences
    pivot_df["absolute_diff"] = pivot_df["direct"] - pivot_df["kueue"]
    pivot_df["percent_diff"] = (pivot_df["absolute_diff"] / pivot_df["direct"]) * 100

    # Extract data for plotting
    job_counts = pivot_df["job_count"].values
    percent_diffs = pivot_df["percent_diff"].values
    absolute_diffs = pivot_df["absolute_diff"].values

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Set x-axis to be logarithmic
    ax1.set_xscale("log", base=2)

    # Plot percentage improvement
    bars1 = ax1.bar(
        job_counts,
        percent_diffs,
        color=["green" if pd > 0 else "red" for pd in percent_diffs],
    )
    ax1.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    ax1.set_ylabel("Improvement (%)", fontsize=14)
    ax1.set_title(
        "Performance Improvement with Kueue vs Direct Kubernetes", fontsize=16
    )
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # Add value labels on top of the bars
    for bar, value in zip(bars1, percent_diffs, strict=False):
        height = bar.get_height()
        text_y_pos = height + 0.5 if height > 0 else height - 3.5
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            text_y_pos,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # Plot absolute time difference
    bars2 = ax2.bar(
        job_counts,
        absolute_diffs,
        color=["green" if ad > 0 else "red" for ad in absolute_diffs],
    )
    ax2.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    ax2.set_xlabel("Number of Jobs", fontsize=14)
    ax2.set_ylabel("Time Saved (seconds)", fontsize=14)
    ax2.set_title("Absolute Time Difference: Direct - Kueue", fontsize=16)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    # Set x-ticks to match the tested job counts
    ax2.set_xticks(job_counts)
    ax2.set_xticklabels([str(int(count)) for count in job_counts], rotation=45)

    # Add value labels on top of the bars
    for bar, value in zip(bars2, absolute_diffs, strict=False):
        height = bar.get_height()
        text_y_pos = height + 5 if height > 0 else height - 15
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            text_y_pos,
            f"{value:.1f}s",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Performance comparison plot saved to {output_file}")


def plot_scaling_efficiency(
    df: pd.DataFrame, output_file: str = "scaling_efficiency.png"
) -> None:
    """
    Plot the scaling efficiency of both approaches.

    Args:
        df: DataFrame containing experiment results
        output_file: Path to save the plot
    """
    # Extract data for direct and Kueue approaches
    direct_df = df[~df["use_kueue"]].sort_values("job_count")
    kueue_df = df[df["use_kueue"]].sort_values("job_count")

    if len(direct_df) < 2 or len(kueue_df) < 2:
        print("Warning: Insufficient data for scaling efficiency plot.")
        return

    # Calculate throughput (jobs per second)
    direct_df["throughput"] = (
        direct_df["job_count"]
        / direct_df["total_time_from_first_creation_to_last_completion"]
    )
    kueue_df["throughput"] = (
        kueue_df["job_count"]
        / kueue_df["total_time_from_first_creation_to_last_completion"]
    )

    # Find the minimum job count present in both datasets
    common_job_counts = set(direct_df["job_count"]) & set(kueue_df["job_count"])
    if not common_job_counts:
        print("Warning: No common job counts between direct and Kueue experiments.")
        return

    min_job_count = min(common_job_counts)

    # Get base throughput values
    direct_base = float(
        direct_df[direct_df["job_count"] == min_job_count]["throughput"].iloc[0]
    )
    kueue_base = float(
        kueue_df[kueue_df["job_count"] == min_job_count]["throughput"].iloc[0]
    )

    # Calculate efficiency
    direct_df["efficiency"] = (direct_df["throughput"] / direct_base) / (
        direct_df["job_count"] / min_job_count
    )
    kueue_df["efficiency"] = (kueue_df["throughput"] / kueue_base) / (
        kueue_df["job_count"] / min_job_count
    )

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot data points with lines
    plt.plot(
        direct_df["job_count"],
        direct_df["efficiency"],
        "bo-",
        linewidth=2,
        label="Direct Kubernetes",
    )
    plt.plot(
        kueue_df["job_count"],
        kueue_df["efficiency"],
        "rx-",
        linewidth=2,
        label="With Kueue",
    )

    # Add a horizontal line at 1.0 for perfect scaling
    plt.axhline(
        y=1.0, color="green", linestyle="--", alpha=0.7, label="Perfect Scaling"
    )

    # Set log scale for x-axis
    plt.xscale("log", base=2)

    # Add labels and title
    plt.xlabel("Number of Jobs", fontsize=14)
    plt.ylabel("Scaling Efficiency", fontsize=14)
    plt.title("Scaling Efficiency Comparison", fontsize=16)

    # Add grid and legend
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)

    # Set x-ticks to match the tested job counts
    all_counts = sorted(set(direct_df["job_count"]) | set(kueue_df["job_count"]))
    plt.xticks(all_counts, [str(int(count)) for count in all_counts], rotation=45)

    # Add value annotations for direct efficiency
    for _i, row in direct_df.iterrows():
        plt.annotate(
            f"{row['efficiency']:.2f}",
            (row["job_count"], row["efficiency"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    # Add value annotations for kueue efficiency
    for _i, row in kueue_df.iterrows():
        plt.annotate(
            f"{row['efficiency']:.2f}",
            (row["job_count"], row["efficiency"]),
            textcoords="offset points",
            xytext=(0, -15),
            ha="center",
        )

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Scaling efficiency plot saved to {output_file}")


def plot_average_job_time(
    df: pd.DataFrame, output_file: str = "avg_job_time.png"
) -> None:
    """
    Plot the average time from job creation to completion.

    Args:
        df: DataFrame containing experiment results
        output_file: Path to save the plot
    """
    # Filter data for direct and kueue runs
    direct_df = df[~df["use_kueue"]]
    kueue_df = df[df["use_kueue"]]

    if direct_df.empty or kueue_df.empty:
        print("Warning: Insufficient data for plotting average job time.")
        return

    # Extract data for plotting
    direct_counts = direct_df["job_count"].values
    direct_times = direct_df["avg_time_from_creation_completion"].values

    kueue_counts = kueue_df["job_count"].values
    kueue_times = kueue_df["avg_time_from_creation_completion"].values

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot data points with lines
    plt.scatter(
        direct_counts,
        direct_times,
        color="blue",
        marker="o",
        s=80,
        label="Direct Kubernetes",
    )
    plt.plot(direct_counts, direct_times, "b-", linewidth=2)

    plt.scatter(
        kueue_counts, kueue_times, color="red", marker="x", s=80, label="With Kueue"
    )
    plt.plot(kueue_counts, kueue_times, "r-", linewidth=2)

    # Set log scale for x-axis
    plt.xscale("log", base=2)

    # Add gridlines
    plt.grid(True, linestyle="--", alpha=0.7)

    # Format axis labels
    plt.xlabel("Number of Jobs", fontsize=14)
    plt.ylabel("Average Job Completion Time (seconds)", fontsize=14)

    # Set plot title
    plt.title("Average Job Completion Time: Direct Kubernetes vs Kueue", fontsize=16)

    # Add legend
    plt.legend(fontsize=12)

    # Set x-ticks to match the tested job counts
    all_counts = sorted(set(direct_counts) | set(kueue_counts))
    plt.xticks(all_counts, [str(int(count)) for count in all_counts], rotation=45)

    # Add value annotations
    for count, time in zip(direct_counts, direct_times, strict=False):
        plt.annotate(
            f"{time:.1f}s",
            (count, time),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    for count, time in zip(kueue_counts, kueue_times, strict=False):
        plt.annotate(
            f"{time:.1f}s",
            (count, time),
            textcoords="offset points",
            xytext=(0, -15),
            ha="center",
        )

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Average job time plot saved to {output_file}")


@app.command("performance")
def performance(
    filepath: str = typer.Option(
        "results.csv", "-f", "--filepath", help="Results CSV File."
    ),
    output_dir: str = typer.Option(
        "./plots", "--output-dir", "-o", help="Output directory for plots"
    ),
    log_scale: bool = typer.Option(
        True,
        "--log-scale/--no-log-scale",
        help="Use logarithmic scale for x-axis in plots",
    ),
):
    """
    Generate visualization plots from benchmark results.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load and clean data
    df = load_and_clean_results(filepath)

    if df.empty:
        print("No data to plot. Please ensure the results file is valid.")
        return

    # Generate plots
    plot_completion_times(
        df,
        output_file=os.path.join(output_dir, "completion_times.png"),
        log_scale=log_scale,
    )

    plot_performance_comparison(
        df, output_file=os.path.join(output_dir, "performance_comparison.png")
    )

    plot_scaling_efficiency(
        df, output_file=os.path.join(output_dir, "scaling_efficiency.png")
    )

    plot_average_job_time(df, output_file=os.path.join(output_dir, "avg_job_time.png"))

    print(f"All plots have been saved to the '{output_dir}' directory.")


if __name__ == "__main__":
    app()
