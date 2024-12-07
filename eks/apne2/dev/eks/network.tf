module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "${local.name}-vpc"
  cidr    = "10.0.0.0/16"

  enable_dns_hostnames      = true
  enable_dns_support      = true
  azs                     = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets         = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
  public_subnets          = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  map_public_ip_on_launch = true
  enable_nat_gateway      = true 
  single_nat_gateway      = true

  public_subnet_tags = {
    "subnet_type" = "public"
  }

  private_subnet_tags = {
    "subnet_type" = "private"
  }
}