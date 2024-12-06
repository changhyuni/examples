# _locals.tf
locals {
  project     = "cacoabank"
  environment = "development"
  azs = ["${var.aws_region}a", "${var.aws_region}b"]
}
