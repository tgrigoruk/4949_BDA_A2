import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

TARGET = "satisfaction"
PATH = "./.model_building/figures/"


def save_plot(filename, save=False):
    plt.savefig(PATH + filename) if save else plt.show()


def plot_heatmap(df, save=False):
    corr = df.corr()
    plt.figure(figsize=(4, 10))
    ax = sns.heatmap(
        corr[[TARGET]].sort_values(by=TARGET, ascending=False),
        linewidth=0.5,
        vmin=-1,
        annot=True,
        vmax=1,
        cmap="YlGnBu",
    )
    plt.tight_layout()
    if save:
        plt.savefig(PATH + "heatmap.png", bbox_inches="tight")
    plt.show()


def pair_plot(df):
    sns.pairplot(df, hue=TARGET, diag_kind="kde")
    plt.show()


def show_scatter_matrix(df, x, y):
    # Create a scatter plot using Seaborn
    sns.scatterplot(x=df[x], y=df[y])

    # Add labels and title
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title("Scatter Plot of {x} vs {y}".format(x=x, y=y))
    plt.show()


def show_boxplot(df, feature, ylabel=None, save=False):
    if not ylabel:
        ylabel = feature
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=TARGET, y=feature, data=df)
    plt.title(f"{feature} Boxplot")
    plt.ylabel(ylabel)
    plt.xlabel(TARGET)

    if save:
        plt.savefig(PATH + "boxplot.png", bbox_inches="tight")
    plt.show()


def show_multiple_boxplots(df, features, ylabel=None, save=False):
    num_features = len(features)
    num_cols = (num_features + 1) // 2
    fig, axes = plt.subplots(nrows=2, ncols=num_cols, figsize=(20, 8))
    axes = axes.flatten()

    for i, feature in enumerate(features):
        sns.boxplot(x=TARGET, y=feature, data=df, ax=axes[i])
        axes[i].set_title(feature)
        axes[i].set_ylabel("")
        axes[i].set_xlabel(TARGET)

    plt.suptitle("Boxplots of Most Significant Features")
    plt.tight_layout()

    if save:
        plt.savefig(PATH + "multiple_boxplots.png", bbox_inches="tight")
    plt.show()


def show_histogram(df, feature, bins=None, title="", save=False):
    plt.title(f"{feature} Histogram")
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    target_color_mapping = {"Low": "blue", "Medium": "green", "High": "red"}

    sns.histplot(
        x=feature,
        hue=TARGET,
        data=df,
        kde=False,
        # palette=target_color_mapping,
        multiple="stack",
    )

    if save:
        plt.savefig(PATH + f"histogram - {feature}.png", bbox_inches="tight")
    plt.show()


def multiple_plots(
    df,
    features,
    plot,
    flip_xy=False,
    title="plot",
    save=False,
):
    num_features = len(features)
    num_rows = 2
    num_cols = (num_features + 1) // 2  # Ensure at least 1 column

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 5 * num_rows))
    axes = axes.flatten()
    # target_color_mapping = {"Low": "blue", "Medium": "green", "High": "red"}

    for i, (ax, feature) in enumerate(zip(axes, features)):
        plot(
            x=feature,
            data=df,
            hue=TARGET,
            ax=ax,
            # palette=target_color_mapping,
            multiple="stack",
        )
        ax.set_title(feature)
        # ax.set_xlabel(feature)
        ax.set_ylabel("")

    # Remove empty subplots
    for j in range(num_features, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()

    if save:
        plt.savefig(PATH + f"multiple_{title}.png", bbox_inches="tight")
    plt.show()
