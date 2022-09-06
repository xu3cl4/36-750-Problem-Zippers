#!/usr/bin/env Rscript

library(testthat)
library(lintr)

## Lint first, ask questions later.
cat("\n--- lintr style checks ---\n")
lint_result <- lint_dir(".")
if (length(lint_result) > 0) {
    cat("\nLinting failed; please check your R style:\n\n")
    print(lint_result)
    cat("\n")
} else {
    cat("All checks passed.\n\n")
}

## test_dir throws an error if there are no tests to run, so e.g. Python
## submissions would have R checks fail, which is unfortunate. Skip R tests if
## there are no R tests.
if (length(find_test_scripts(".")) > 0) {
    cat("--- testthat unit tests ---\n\n")
    test_dir(".", stop_on_failure = TRUE, reporter = CheckReporter)
} else {
    cat("\nNo R tests found! Skipping R testing.\n")
}

if (length(lint_result) > 0) {
    ## Non-zero exit status to make CI fail.
    q(status = 11)
}
