import sys

from bedalyze import analyze_bed

if len(sys.argv) != 2:
    print("Usage: python main.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

avg_width, std_width, var_width, avg_score, std_score, var_score = analyze_bed(file_path)

print(f"Avg region width: {avg_width:.2f}, Std: {std_width:.2f}, Var: {var_width:.2f}")
print(f"Avg score: {avg_score:.2f}, Std: {std_score:.2f}, Var: {var_score:.2f}")
