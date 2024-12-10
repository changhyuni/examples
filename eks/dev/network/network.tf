module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "${local.name}-vpc"
  cidr    = "10.0.0.0/16"

  enable_dns_hostnames    = true
  enable_dns_support      = true
  azs                     = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  private_subnets         = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
  ## ALB Controller 실습 때 서브넷 두개 이상  필요
  public_subnets          = ["10.0.1.0/24", "10.0.2.0/24"]
  map_public_ip_on_launch = true
  enable_nat_gateway      = true 
  single_nat_gateway      = true

  public_subnet_tags = {
    "subnet_type" = "public",

    # ALB Controller 실습 때 사용
    "kubernetes.io/role/elb" = "1",
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "subnet_type" = "private",
    # ALB Controller 실습 때 사용
    "kubernetes.io/role/internal-elb" = "1",
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }
}