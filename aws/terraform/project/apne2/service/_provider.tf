# _provider.tf
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
    Project     = local.project
    Environment = local.environment
    ManagedBy   = "Terraform"
    }    
  }
}
