module "public_nodegroup" {
  source                      = "../../../modules/nodegroup"
  nodegroup_name              = "${local.name}-public-nodegroup"
  eks_cluster_name            = "${local.name}-cluster"
  vpc_subnet_ids              = module.vpc.public_subnets
  eks_nodes_keypair_name      = local.keypair_name

  node_security_group_ids = [
    aws_security_group.public_node.id,
    module.cluster.eks_cluster_security_group_id
  ]

  depends_on = [ 
    module.cluster,
    module.vpc,
    aws_security_group.public_node,
    aws_key_pair.key_pair
  ]
}

module "private_nodegroup" {
  source                      = "../../../modules/nodegroup"
  nodegroup_name              = "${local.name}-private-nodegroup"
  eks_cluster_name            = "${local.name}-cluster"
  vpc_subnet_ids              = module.vpc.private_subnets
  eks_nodes_keypair_name      = local.keypair_name

  node_security_group_ids = [
    aws_security_group.private_node.id,
    module.cluster.eks_cluster_security_group_id
  ]

  depends_on = [ 
    module.cluster,
    module.vpc,
    aws_security_group.private_node,
    aws_key_pair.key_pair
  ]
}
