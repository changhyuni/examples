module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
  name    = local.project
  cidr    = "10.0.0.0/16"

  enable_dns_hostnames = true
  enable_dns_support   = true
  azs                  = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets       = ["10.0.101.0/24"]
  enable_nat_gateway   = true # Required as k8s hosts will be in privat_subnet
  enable_vpn_gateway   = false
  single_nat_gateway   = true # NAT GW is required as nodes will be provisioned in private subnet

  public_subnet_tags = {
    "subnet_type"            = "public"
  }

  private_subnet_tags = {
    "subnet_type"                     = "private"
  }
}