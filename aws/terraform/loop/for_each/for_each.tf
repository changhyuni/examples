variable "user_names" {
  type = map(string)
  default = {
    "june" = "Kubernetes Engineer"
    "rex" = "Cloud Engineer"
  }
}

resource "aws_iam_user" "iam" {
  for_each = var.user_names
  name = each.key
  tags = {
    "Role"     = each.value
  }
}

output "iam_user_arns" {
  description = "List of all IAM user ARNs"
#   value       = aws_iam_user.iam
#   value       = { for k, v in aws_iam_user.iam : k => v.arn }
  value       = [ for _, v in aws_iam_user.iam : v.arn ]
}