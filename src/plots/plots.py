import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_author_feature_distributions(df: pd.DataFrame, aggregate: str = "mean"):
    """
    Draws bar charts and violin plots for all numeric columns in the dataframe,
    grouped by the 'author' column.
    """
    if "author" not in df.columns:
        raise ValueError("The dataframe must contain a column named 'author'.")


    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric features found to plot.")

    sns.set(style="whitegrid")
    
    for col in numeric_cols:
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        aggregated = df.groupby("author")[col].agg(aggregate).sort_values()
        sns.barplot(x=aggregated.index, y=aggregated.values, palette="Set2")
        plt.title(f"{col} \u2014 {aggregate} by author")
        plt.xticks(rotation=45)
        plt.ylabel(col)
        plt.xlabel("Author")

        plt.subplot(1, 2, 2)
        sns.violinplot(data=df, x="author", y=col, palette="Set3", inner="quartile")
        plt.title(f"{col} \u2014 Distribution by author")
        plt.xticks(rotation=45)
        plt.ylabel(col)
        plt.xlabel("Author")

        plt.tight_layout()
        plt.show()
        
def plot_clusters(result_df: pd.DataFrame):
    """
    Plot t-SNE results colored by author and shaped by cluster.
    """
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=result_df,
        x='tsne_1',
        y='tsne_2',
        style='author' if 'author' in result_df.columns else None,
        hue='cluster' if 'cluster' in result_df.columns else None,
        palette='tab10',
        alpha=0.7,
        s=80
    )

    if 'title' in result_df.columns:
        for i in range(0, len(result_df), max(1, len(result_df) // 100)):
            plt.text(result_df.loc[i, 'tsne_1'], result_df.loc[i, 'tsne_2'],
                     str(result_df.loc[i, 'title'])[:30], fontsize=8, alpha=0.6)

    plt.title(f"t-SNE Visualization with KMeans Clusters (k={result_df['cluster'].nunique() if 'cluster' in result_df.columns else '?'})")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.legend(title='Author', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()