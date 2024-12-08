
locals {
  enabled              = var.enabled
  eks_cluster_id       = aws_eks_cluster.this[0].name

  eks_policy_short_abbreviation_map = {
    Admin        = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy"
    ClusterAdmin = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
    Edit         = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy"
    View         = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy"
  }

  eks_policy_abbreviation_map = merge(
    { for k, v in local.eks_policy_short_abbreviation_map : format("AmazonEKS%sPolicy", k) => v },
    local.eks_policy_short_abbreviation_map
  )

  access_entry_expanded_map = {
    for k, v in var.access_entry_map : k => merge({
      access_policy_associations = {
        for kk, vv in v.access_policy_associations :
        try(local.eks_policy_abbreviation_map[kk], kk) => vv
      }
    },
    { for kk, vv in v : kk => vv if kk != "access_policy_associations" })
  }

  access_entry_map = {
    for k, v in local.access_entry_expanded_map : k => merge({
      kubernetes_groups = [
        for group in v.kubernetes_groups :
        group if group != "system:masters" || v.type != "STANDARD"
      ]
      access_policy_associations = merge(
        v.access_policy_associations,
        contains(v.kubernetes_groups, "system:masters") && v.type == "STANDARD" ? {
          "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy" = {
            access_scope = {
              type       = "cluster"
              namespaces = null
            }
          }
        } : {}
      )
    },
    { for kk, vv in v : kk => vv if kk != "kubernetes_groups" && kk != "access_policy_associations" })
  }

  eks_access_policy_association_product_map = merge(flatten([
    for k, v in local.access_entry_map : [
      for kk, vv in v.access_policy_associations : {
        format("%s-%s", k, kk) = {
          principal_arn = k
          policy_arn    = kk
        }
      }
    ]
  ])...)
}

# Key-based Access Entries
resource "aws_eks_access_entry" "map" {
  for_each = local.enabled ? local.access_entry_map : {}
  cluster_name      = local.eks_cluster_id
  principal_arn     = each.key
  kubernetes_groups = each.value.kubernetes_groups
  type              = each.value.type
  tags              = var.tags

  depends_on = [ aws_eks_cluster.this ]
}

resource "aws_eks_access_policy_association" "map" {
  for_each    = local.enabled ? local.eks_access_policy_association_product_map : {}
  cluster_name  = local.eks_cluster_id
  principal_arn = each.value.principal_arn
  policy_arn    = each.value.policy_arn

  access_scope {
    type       = local.access_entry_map[each.value.principal_arn].access_policy_associations[each.value.policy_arn].access_scope.type
    namespaces = local.access_entry_map[each.value.principal_arn].access_policy_associations[each.value.policy_arn].access_scope.namespaces
  }

  depends_on = [ aws_eks_cluster.this ]
}