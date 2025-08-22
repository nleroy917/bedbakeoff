# BED bakeoff
Just experimenting with different ways to read in and analyze BED files.

To time things, I enter the appropriate directory and run:
```
time Rscript main.R ../data/example.bed.gz
time python main.py ../data/example.bed.gz
time cargo run --release -- ../data/example.bed.gz
```