resource "aws_eks_addon" "this" {
  for_each = var.enabled && length(var.addons) > 0 ? { for addon in var.addons : addon.addon_name => addon } : {}
  cluster_name                = var.cluster_name
  addon_name                  = each.key
  addon_version               = lookup(each.value, "addon_version", null)
  configuration_values        = lookup(each.value, "configuration_values", null)
  resolve_conflicts_on_create = lookup(each.value, "resolve_conflicts_on_create", try(replace(each.value.resolve_conflicts, "PRESERVE", "NONE"), null))
  resolve_conflicts_on_update = lookup(each.value, "resolve_conflicts_on_update", lookup(each.value, "resolve_conflicts", null))
  service_account_role_arn    = lookup(each.value, "service_account_role_arn", null)

  tags = var.tags

  timeouts {
    create = each.value.create_timeout
    update = each.value.update_timeout
    delete = each.value.delete_timeout
  }
}