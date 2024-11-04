variable "user_names" {
  type    = list(string)
  default = ["june", "robin", "rex"]
}

resource "aws_iam_user" "iam" {
  count = length(var.user_names)
  name  = var.user_names[count.index]
}

output "iam_user_arns" {
  description = "List of all IAM user ARNs"
  value       = aws_iam_user.iam
}

output "iam_user_arns_index" {
  description = "List of all IAM user ARNs"
  value       = aws_iam_user.iam[0].arn
}