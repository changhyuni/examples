resource "aws_eks_cluster" "this" {
  count                      = var.enabled ? 1 : 0
  name                       = var.cluster_name
  version                    = var.cluster_version
  role_arn                   = aws_iam_role.eks_cluster_role.arn
  tags                       = var.tags
  enabled_cluster_log_types  = var.enabled_cluster_log_types

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = var.endpoint_private_access
    endpoint_public_access  = var.endpoint_public_access
    public_access_cidrs     = var.public_access_cidrs
    security_group_ids      = length(var.security_group_ids) > 0 ? var.security_group_ids : null
  }
  
  bootstrap_self_managed_addons = true

  access_config {
    authentication_mode = var.access_config.authentication_mode
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy_attachment,
    aws_iam_role_policy_attachment.eks_service_policy_attachment,
    aws_iam_role.eks_cluster_role
  ]

  kubernetes_network_config {
    service_ipv4_cidr = var.service_ipv4_cidr
  }
}