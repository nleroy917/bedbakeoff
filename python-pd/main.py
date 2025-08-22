import sys

from time import time

import pandas as pd

def main():
    start = time()
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_path = "../data/example.bed.gz"

    df = pd.read_csv(
        file_path,
        sep="\t",
        header=None,
        names=["chr", "start", "end", "name", "score"],
        dtype={"chr": str, "start": int, "end": int, "name": str, "score": float},
        engine="pyarrow",
        dtype_backend="pyarrow"
    )

    # calculate region widths and statistics using Pandas
    df["width"] = df["end"] - df["start"]
    stats_df = df[["width", "score"]].agg(["mean", "std", "var"]).T
    
    # extract values for printing
    avg_width = stats_df.loc["width", "mean"]
    std_width = stats_df.loc["width", "std"]
    var_width = stats_df.loc["width", "var"]
    avg_score = stats_df.loc["score", "mean"]
    std_score = stats_df.loc["score", "std"]
    var_score = stats_df.loc["score", "var"]

    print(f"Avg region width: {avg_width:.2f}, Std: {std_width:.2f}, Var: {var_width:.2f}")
    print(f"Avg score: {avg_score:.2f}, Std: {std_score:.2f}, Var: {var_score:.2f}")
    end = time()
    print(f"Time taken: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
