from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import typer

sns.set(style="whitegrid")

app = typer.Typer(help="Plot Kueue Benchmark Results")


# Load CSV into DataFrame
def load_results(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        parse_dates=[
            "timestamp",
            "first_creation_time",
            "last_creation_time",
            "first_completion_time",
            "last_completion_time",
        ],
    )
    return df


# Compute throughput
def compute_throughput(df: pd.DataFrame) -> pd.DataFrame:
    df["throughput"] = df["job_count"] / df["total_execution_time"]
    return df


# Compute startup and completion latency
def compute_latency(df: pd.DataFrame) -> pd.DataFrame:
    df["startup_latency"] = (
        df["first_completion_time"] - df["first_creation_time"]
    ).dt.total_seconds()
    df["completion_latency"] = (
        df["last_completion_time"] - df["last_creation_time"]
    ).dt.total_seconds()
    return df


# Compute coefficient of variation (CV)
def compute_cv(df: pd.DataFrame) -> pd.DataFrame:
    df["cv"] = (
        df["std_dev_time_from_creation_completion"]
        / df["avg_time_from_creation_completion"]
    )
    return df


# Calculate comparative improvements
def compute_comparative_metrics(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("use_kueue").mean(numeric_only=True)
    comparisons = pd.DataFrame(
        {
            "throughput_improvement": 100
            * (grouped.loc[True, "throughput"] - grouped.loc[False, "throughput"])
            / grouped.loc[False, "throughput"],
            "avg_duration_improvement": 100
            * (
                grouped.loc[False, "avg_time_from_creation_completion"]
                - grouped.loc[True, "avg_time_from_creation_completion"]
            )
            / grouped.loc[False, "avg_time_from_creation_completion"],
            "median_duration_improvement": 100
            * (
                grouped.loc[False, "median_time_from_creation_completion"]
                - grouped.loc[True, "median_time_from_creation_completion"]
            )
            / grouped.loc[False, "median_time_from_creation_completion"],
        },
        index=[0],
    )
    return comparisons


# Plot metrics
def plot_metric_comparison(
    df: pd.DataFrame, metric: str, ylabel: str, title: str
) -> None:
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x="use_kueue", y=metric)
    plt.xlabel("Using Kueue")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks([0, 1], ["No", "Yes"])
    plt.show()


# Plot distributions of job durations
def plot_duration_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    sns.histplot(
        df, x="avg_time_from_creation_completion", hue="use_kueue", kde=True, bins=20
    )
    plt.xlabel("Average Job Duration (s)")
    plt.title("Distribution of Average Job Durations")
    plt.show()


# Plot completion times with trendlines on log-scale
def plot_completion_times(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    df["completion_time_seconds"] = (
        df["last_completion_time"] - df["first_creation_time"]
    ) / np.timedelta64(1, "s")
    sns.scatterplot(
        data=df,
        x="completion_time_seconds",
        y="job_count",
        hue="use_kueue",
        style="use_kueue",
    )
    sns.regplot(
        data=df[df["use_kueue"] is False],
        x="completion_time_seconds",
        y="job_count",
        scatter=False,
        logx=True,
        label="Trendline (No Kueue)",
    )
    sns.regplot(
        data=df[df["use_kueue"] is True],
        x="completion_time_seconds",
        y="job_count",
        scatter=False,
        logx=True,
        label="Trendline (Kueue)",
    )
    plt.ylabel("Job Count")
    plt.xlabel("Completion Time (Seconds, Log scale)")
    plt.xscale("log")
    plt.title("Job Completion Times with Trendlines (Log scale)")
    plt.legend()
    plt.tight_layout()
    plt.show()


# Plot scaling efficiency
def plot_scaling_efficiency(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="job_count", y="throughput", hue="use_kueue", marker="x")
    plt.xlabel("Number of Jobs")
    plt.ylabel("Efficiency (Jobs per Second)")
    plt.title("Efficiency Comparison with Scaling")
    plt.legend(title="Using Kueue", labels=["No", "Yes"])
    plt.tight_layout()
    plt.show()


# Visualization function
def plot_scheduling_overhead(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="use_kueue", y="scheduling_overhead")
    plt.xticks([0, 1], ["No", "Yes"])
    plt.xlabel("Using Kueue")
    plt.ylabel("Scheduling Overhead (seconds)")
    plt.title("Comparison of Job Scheduling Overhead")
    plt.show()


def compute_scheduling_overhead(df: pd.DataFrame) -> pd.DataFrame:
    df["scheduling_overhead"] = (
        df["first_completion_time"] - df["first_creation_time"]
    ).dt.total_seconds() - df["job_duration"]
    return df


@app.command("performance")
def analyze_and_plot(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = load_results(filepath)
    df = compute_throughput(df)
    df = compute_latency(df)
    df = compute_cv(df)
    df = compute_scheduling_overhead(df)
    comparative_df = compute_comparative_metrics(df)
    plot_metric_comparison(df, "throughput", "Jobs per Second", "Throughput Comparison")
    plot_metric_comparison(
        df, "startup_latency", "Latency (seconds)", "Startup Latency Comparison"
    )
    plot_metric_comparison(
        df, "completion_latency", "Latency (seconds)", "Completion Latency Comparison"
    )
    plot_metric_comparison(df, "cv", "Coefficient of Variation", "CV of Job Durations")
    plot_duration_distribution(df)
    plot_completion_times(df)
    plot_scaling_efficiency(df)
    plot_scheduling_overhead(df)

    return df, comparative_df
