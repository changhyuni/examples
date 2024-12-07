module "addons" {
  source                    = "../modules/addons"
  enabled                   = true
  cluster_name              = "${local.name}-cluster"

  # Optional variables
  addons                     = local.addons
  depends_on = [ 
    module.vpc,
    module.cluster,
    module.private_nodegroup,
    module.public_nodegroup 
  ]
}