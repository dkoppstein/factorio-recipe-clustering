library(tidyverse)
library(ComplexHeatmap)
library(circlize)

df <- readr::read_csv("recipe.csv")

df <- df %>% dplyr::filter(!grepl("ee-", X1)) %>% dplyr::filter(!grepl("textplate", X1)) %>% dplyr::filter(!grepl("ore", X1))# for some random modded stuff

df <- df %>% dplyr::select(!starts_with("ee-")) %>% dplyr::select(!starts_with("text"))

# df_boolean <- df %>% mutate_if(is.numeric, ~1 * (. > 0))

col_fun = circlize::colorRamp2(c(0, 50), c("white", "red"))

make_matrix <- function(df, rownames = NULL) {
  my_matrix <-  as.matrix(df)
  if(!is.null(rownames))
    rownames(my_matrix) = rownames
  my_matrix
}

mat <- make_matrix(dplyr::select(df, -X1), pull(df, X1))

pdf("heatmap.pdf", width = 48, height = 48)
ht <- ComplexHeatmap::Heatmap(mat, col = col_fun, cluster_rows = TRUE, clustering_distance_rows = "pearson", cluster_columns = FALSE, row_dend_side = "right", row_dend_width = unit(8, "in"))
draw(ht)
dev.off()
