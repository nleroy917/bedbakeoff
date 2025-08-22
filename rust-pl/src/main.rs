use std::sync::Arc;

use polars::prelude::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <file_path>", args[0]);
        std::process::exit(1);
    }
    let file_path = &args[1];

    let bed_schema = Arc::new(Schema::from_iter(vec![
        Field::new("chr".into(), DataType::String),
        Field::new("start".into(), DataType::UInt32),
        Field::new("end".into(), DataType::UInt32),
        Field::new("name".into(), DataType::String),
        Field::new("score".into(), DataType::Float64)
    ]));

    let stats_df = LazyCsvReader::new(PlPath::new(file_path))
        .with_has_header(false)
        .with_separator(b'\t')
        .with_schema(Some(bed_schema))
        .finish()?
        .select(&[
            (col("end") - col("start")).alias("width"),
            col("score")
        ])
            .select(&[
            // width statistics
            col("width").mean().alias("avg_width"),
            col("width").std(1).alias("std_width"),
            col("width").var(1).alias("var_width"),
            // score statistics
            col("score").mean().alias("avg_score"),
            col("score").std(1).alias("std_score"),
            col("score").var(1).alias("var_score")
        ])
        .collect()?;


    println!("{:?}", stats_df);
    
    Ok(())
}
