# _provider.tf
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      ManagedBy   = "Terraform"
    }    
  }
}

terraform {
  backend "s3" {
    bucket = "junetf-bucket"
    key    = "terraform/dev/network/terraform.tfstate"
    region = "ap-northeast-2"
  }
}