# _locals.tf
locals {
  ## Common Configs
  name           = "${var.environment}-${var.project}"
}