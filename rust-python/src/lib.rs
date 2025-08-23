use std::fs::File;
use std::io::{BufRead, BufReader};

use flate2::read::GzDecoder;

use pyo3::prelude::*;

#[pyfunction]
pub fn analyze_bed(file_path: String) -> (f64, f64, f64, f64, f64, f64) {
    let file = File::open(file_path).unwrap();
    let gz_decoder = GzDecoder::new(file);
    let reader = BufReader::new(gz_decoder);

    let mut count = 0;
    let mut width_sum = 0u64;
    let mut width_sum_sq = 0f64;
    let mut score_sum = 0f64;
    let mut score_sum_sq = 0f64;

    for line in reader.lines() {
        let line = line.unwrap();
        let fields: Vec<&str> = line.trim().split('\t').collect();
        
        if fields.len() >= 5 {
            let start = fields[1].parse::<u32>().unwrap();
            let end = fields[2].parse::<u32>().unwrap();
            let score = fields[4].parse::<f64>().unwrap();
            
            let width = end - start;
            
            count += 1;
            width_sum += width as u64;
            width_sum_sq += (width as f64).powi(2);
            score_sum += score;
            score_sum_sq += score.powi(2);
        }
    }

    let n = count as f64;
    
    let avg_width = width_sum as f64 / n;
    let var_width = (width_sum_sq / n) - avg_width.powi(2);
    let std_width = var_width.sqrt();

    let avg_score = score_sum / n;
    let var_score = (score_sum_sq / n) - avg_score.powi(2);
    let std_score = var_score.sqrt();

    (avg_width, std_width, var_width, avg_score, std_score, var_score)

}

/// A Python module implemented in Rust.
#[pymodule]
fn bedalyze(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(analyze_bed, m)?)?;
    Ok(())
}
