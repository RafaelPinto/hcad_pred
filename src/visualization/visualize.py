import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y


def plot_ecdf(series, xlabel, ylabel='ECDF', title=None, figsize=(8, 8)):
    """Plot ecdf from series"""
    x, y = ecdf(series)

    quantiles_y = [0.1, 0.25, 0.5, 0.75, 0.9]
    quantiles_x = np.quantile(x, quantiles_y)

    fig, ax = plt.subplots(figsize=figsize)
    plt.plot(x, y, marker='.', linestyle='none')
    plt.plot(quantiles_x, quantiles_y, marker='D',
             linestyle='none', color='blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(('ECDF', 'Quantiles'), loc='lower right')

    if title:
        plt.title(title)

    print(f"Quantile 10%: {quantiles_x[0]:.2f}")
    print(f"Quantile 25%: {quantiles_x[1]:.2f}")
    print(f"Quantile 50%: {quantiles_x[2]:.2f}")
    print(f"Quantile 75%: {quantiles_x[3]:.2f}")
    print(f"Quantile 90%: {quantiles_x[4]:.2f}")
    return


def plot_counts(series, xlabel, title=None, figsize=(8, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    sns.countplot(series, order=series.value_counts().index)
    plt.xticks(rotation=90)

    if title:
        plt.title(title)

    return


def plot_hist(series, xlabel, title=None, figsize=(8, 8), bins=5):
    fig, ax = plt.subplots(figsize=(8, 8))
    series.hist(histtype='stepfilled', linewidth=2, bins=bins, grid=False)
    plt.xlabel(xlabel)
    plt.ylabel('Count')

    if title:
        plt.title(title)

    return
