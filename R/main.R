library(data.table)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  if (!length(args)) { cat("Usage: Rscript main.R [file_path]\n"); quit(status = 1) }
  file_path <- args[1]

  # read only starts (V2), ends (V3), scores (V5); set types to integer/numeric
  DT <- fread(file_path,
              col.names = c("chr","start","end","name","score"),
              colClasses = c("character","integer","integer","character","numeric"),
              showProgress = FALSE)

  widths <- DT$end - DT$start

  avg_width <- mean(widths)
  std_width <- sd(widths)
  var_width <- var(widths)

  avg_score <- mean(DT$score)
  std_score <- sd(DT$score)
  var_score <- var(DT$score)

  cat(sprintf("Avg region width: %.2f, Std: %.2f, Var: %.2f\n",
              avg_width, std_width, var_width))
  cat(sprintf("Avg score: %.2f, Std: %.2f, Var: %.2f\n",
              avg_score, std_score, var_score))
}
main()