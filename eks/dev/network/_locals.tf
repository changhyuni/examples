# _locals.tf
locals {
  ## Common Configs
  name           = "${var.environment}-${var.project}"
  cluster_name   = "${var.environment}-${var.project}-cluster"
}