module "nodegroup" {
  source            = "./modules/nodegroup"
  environment       = local.environment
  nodegroup_name    = local.project
  eks_cluster_name  = "my-eks-cluster"
  vpc_subnet_ids    = ["subnet-abc123456", "subnet-def789012"]

  worker_iam_role_arn = aws_iam_role.node_role.arn
}
