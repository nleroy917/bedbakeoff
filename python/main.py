import gzip
import math
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    # initialize counters for streaming statistics
    count = 0
    width_sum = width_sum_sq = 0
    score_sum = score_sum_sq = 0
    
    with gzip.open(file_path, "rb") as file:
        for line in file.readlines():
            fields = line.decode().strip().split("\t")
            start = int(fields[1])
            end = int(fields[2])
            score = float(fields[4])
            
            width = end - start
            
            count += 1
            width_sum += width
            width_sum_sq += width ** 2
            score_sum += score
            score_sum_sq += score ** 2
    
    if count > 0:
        # calculate statistics
        avg_width = width_sum / count
        var_width = (width_sum_sq / count) - (avg_width ** 2)
        std_width = math.sqrt(var_width) if var_width >= 0 else 0
        
        avg_score = score_sum / count
        var_score = (score_sum_sq / count) - (avg_score ** 2)
        std_score = math.sqrt(var_score) if var_score >= 0 else 0
        
        print(f"Avg region width: {avg_width:.2f}, Std: {std_width:.2f}, Var: {var_width:.2f}")
        print(f"Avg score: {avg_score:.2f}, Std: {std_score:.2f}, Var: {var_score:.2f}")
    else:
        print("No data found in file")


if __name__ == "__main__":
    main()
