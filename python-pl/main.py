import polars as pl


def read_bed(file_path: str) -> pl.DataFrame:
    """
    Read in a bed file and return a Polars DataFrame

    Args:
        file_path (str): The path to the bed file to read.

    Returns:
        pl.DataFrame: DataFrame containing bed file data with columns: chr, start, end, name, score
    """
    return pl.read_csv(
        file_path,
        separator="\t",
        has_header=False,
        new_columns=["chr", "start", "end", "name", "score"],
        schema_overrides={"chr": pl.Utf8, "start": pl.Int64, "end": pl.Int64, "name": pl.Utf8, "score": pl.Float64}
    )


def main():
    file_path = "../data/example.bed.gz"
    
    df = read_bed(file_path)
    
    # Calculate region widths and statistics using Polars
    stats_df = df.select([
        (pl.col("end") - pl.col("start")).alias("width"),
        pl.col("score")
    ]).select([
        # Width statistics
        pl.col("width").mean().alias("avg_width"),
        pl.col("width").std().alias("std_width"),
        pl.col("width").var().alias("var_width"),
        # Score statistics
        pl.col("score").mean().alias("avg_score"),
        pl.col("score").std().alias("std_score"),
        pl.col("score").var().alias("var_score")
    ])
    
    # Extract values for printing
    stats = stats_df.row(0)
    avg_width, std_width, var_width, avg_score, std_score, var_score = stats
    
    print(f"Avg region width: {avg_width:.2f}, Std: {std_width:.2f}, Var: {var_width:.2f}")
    print(f"Avg score: {avg_score:.2f}, Std: {std_score:.2f}, Var: {var_score:.2f}")


if __name__ == "__main__":
    main()
