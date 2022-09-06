#!/usr/bin/env Rscript
## Run this script with, for example,
## Rscript check.R assignment-name
## from within your assignments repository.

library(lintr)
library(testthat)

assignment_name <- commandArgs(TRUE)

setwd(assignment_name)

cat("\nLinting:\n")
lint_dir(".")

cat("\n\nTesting:\n")
test_dir(".")
