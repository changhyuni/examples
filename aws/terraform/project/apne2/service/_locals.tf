# _locals.tf

locals {
  project     = "june"
  environment = "development"
  azs = ["${var.aws_region}a", "${var.aws_region}b"]
}
