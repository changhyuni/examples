# _locals.tf
locals {
  ## Common Configs
  name           = "${var.environment}-${var.project}"
  my_ip          = "61.78.133.233/32"
  keypair_name   = "${var.environment}-${var.project}-keypair"  

  ## EKS Cluster Configs
  addons = [
    {
      addon_name    = "kube-proxy"
      addon_version = "v1.30.6-eksbuild.3"
    },
    {
      addon_name    = "coredns"
      addon_version = "v1.11.1-eksbuild.8"
    },
  ]

  access_config = {
    authentication_mode                         = "API_AND_CONFIG_MAP"
    bootstrap_cluster_creator_admin_permissions = false
  }

  access_entry_map = {
    "arn:aws:iam::357836924303:user/admin" = {
    # kubernetes_groups = ["system:masters"]
      type              = "STANDARD"
      access_policy_associations = {
        "Admin" = {
          access_scope = {
            type       = "cluster"
            namespaces = null
          }
        }
      }
    }
  }
}