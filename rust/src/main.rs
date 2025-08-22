use std::fs::File;
use std::io::{BufRead, BufReader};
use flate2::read::GzDecoder;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <file_path>", args[0]);
        std::process::exit(1);
    }
    let file_path = &args[1];

    let file = File::open(file_path)?;
    let gz_decoder = GzDecoder::new(file);
    let reader = BufReader::new(gz_decoder);

    let mut count = 0;
    let mut width_sum = 0u64;
    let mut width_sum_sq = 0f64;
    let mut score_sum = 0f64;
    let mut score_sum_sq = 0f64;

    for line in reader.lines() {
        let line = line?;
        let fields: Vec<&str> = line.trim().split('\t').collect();
        
        if fields.len() >= 5 {
            let start = fields[1].parse::<u32>()?;
            let end = fields[2].parse::<u32>()?;
            let score = fields[4].parse::<f64>()?;
            
            let width = end - start;
            
            count += 1;
            width_sum += width as u64;
            width_sum_sq += (width as f64).powi(2);
            score_sum += score;
            score_sum_sq += score.powi(2);
        }
    }

    if count > 0 {
        let n = count as f64;
        
        let avg_width = width_sum as f64 / n;
        let var_width = (width_sum_sq / n) - avg_width.powi(2);
        let std_width = var_width.sqrt();

        let avg_score = score_sum / n;
        let var_score = (score_sum_sq / n) - avg_score.powi(2);
        let std_score = var_score.sqrt();

        println!("Avg region width: {:.2}, Std: {:.2}, Var: {:.2}", avg_width, std_width, var_width);
        println!("Avg score: {:.2}, Std: {:.2}, Var: {:.2}", avg_score, std_score, var_score);
    } else {
        println!("No valid data found");
    }

    Ok(())
}
