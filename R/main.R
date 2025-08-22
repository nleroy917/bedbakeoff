read_bed <- function(file_path) {
    
    data <- read.table(gzfile(file_path), header = FALSE, stringsAsFactors = FALSE)

    chrs <- data$V1
    starts <- data$V2
    ends <- data$V3
    names <- data$V4
    scores <- data$V5

    return(list(chrs = chrs, starts = starts, ends = ends, names = names, scores = scores))
}

printHelpAndExit <- function() {
    cat("Usage: Rscript main.R [file_path]\n")
    quit(status = 1)
}

main <- function() {
    args <- commandArgs(trailingOnly = TRUE)
    file_path <- if (length(args) > 0) args[1] else printHelpAndExit()
    
    bed_data <- read_bed(file_path)
    starts <- bed_data$starts
    ends <- bed_data$ends
    scores <- bed_data$scores
    
    # get region widths
    widths <- ends - starts
    
    # statistics for widths
    avg_width <- mean(widths)
    std_width <- sd(widths)
    var_width <- var(widths)
    
    # statistics for scores
    avg_score <- mean(scores)
    std_score <- sd(scores)
    var_score <- var(scores)
    
    # print results
    cat(sprintf("Avg region width: %.2f, Std: %.2f, Var: %.2f\n", 
                            avg_width, std_width, var_width))
    cat(sprintf("Avg score: %.2f, Std: %.2f, Var: %.2f\n", 
                            avg_score, std_score, var_score))
}

# run main function
main()