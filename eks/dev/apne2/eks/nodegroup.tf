module "private_nodegroup" {
  source                      = "../../../modules/nodegroup"
  nodegroup_name              = "${local.name}-private-nodegroup"
  eks_cluster_name            = "${local.name}-cluster"
  vpc_subnet_ids              = local.private_subnets
  eks_nodes_keypair_name      = local.keypair_name

  nodegroup_desired_size      = local.node_size
  nodegroup_max_size          = local.node_max_size
  nodegroup_min_size          = local.node_min_size
  nodegroup_instance_types    = local.node_type

  node_security_group_ids = [
    aws_security_group.private_node.id,
    module.cluster.eks_cluster_security_group_id
  ]

  depends_on = [ 
    module.cluster,
    aws_security_group.private_node,
    aws_key_pair.key_pair
  ]
}

# module "public_nodegroup" {
#   source                      = "../../../modules/nodegroup"
#   nodegroup_name              = "${local.name}-public-nodegroup"
#   eks_cluster_name            = "${local.name}-cluster"
#   vpc_subnet_ids              = local.public_subnets
#   eks_nodes_keypair_name      = local.keypair_name

#   node_security_group_ids = [
#     aws_security_group.public_node.id,
#     module.cluster.eks_cluster_security_group_id
#   ]

#   depends_on = [ 
#     module.cluster,
#     aws_security_group.public_node,
#     aws_key_pair.key_pair
#   ]
# }