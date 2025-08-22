import sys

import polars as pl

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    df = pl.read_csv(
        file_path,
        separator="\t",
        has_header=False,
        new_columns=["chr", "start", "end", "name", "score"],
        schema_overrides={"chr": pl.Utf8, "start": pl.Int64, "end": pl.Int64, "name": pl.Utf8, "score": pl.Float64}
    )
    
    # calculate region widths and statistics using Polars
    stats_df = df.select([
        (pl.col("end") - pl.col("start")).alias("width"),
        pl.col("score")
    ]).select([
        # width statistics
        pl.col("width").mean().alias("avg_width"),
        pl.col("width").std().alias("std_width"),
        pl.col("width").var().alias("var_width"),
        # score statistics
        pl.col("score").mean().alias("avg_score"),
        pl.col("score").std().alias("std_score"),
        pl.col("score").var().alias("var_score")
    ])
    
    # extract values for printing
    stats = stats_df.row(0)
    avg_width, std_width, var_width, avg_score, std_score, var_score = stats
    
    print(f"Avg region width: {avg_width:.2f}, Std: {std_width:.2f}, Var: {var_width:.2f}")
    print(f"Avg score: {avg_score:.2f}, Std: {std_score:.2f}, Var: {var_score:.2f}")


if __name__ == "__main__":
    main()
