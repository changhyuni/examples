module "cluster" {
  source                    = "../../../modules/cluster"
  enabled                   = true
  cluster_name              = "${local.name}-cluster"
  cluster_version           = "1.30"
  subnet_ids                = module.vpc.private_subnets
  
  # Optional variables
  endpoint_public_access     = true
  endpoint_private_access    = true
  public_access_cidrs        = [local.my_ip]
  security_group_ids         = [aws_security_group.cluster_private_access.id]
  access_config              = local.access_config
  access_entry_map           = local.access_entry_map

  depends_on = [ module.vpc ]
}