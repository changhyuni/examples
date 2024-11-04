variable "user_roles" {
  type = map(object({
    role = string
    age  = number
  }))
  default = {
    "june" = {
      role = "Kubernetes Engineer"
      age  = 30
    }
    "robin" = {
      role = "Kubernetes Engineer"
      age  = 28
    }
    "rex" = {
      role = "Cloud Engineer"
      age  = 36
    }
  }
}

resource "aws_iam_user" "myiam" {
  for_each = var.user_roles

  name = each.key

  tags = {
    "Role" = each.value.role
    "UserStatus" = each.value.age > 35 ? "Senior" : "Junior"
  }
}

output "user_statuses" {
  value = {
    for user, details in var.user_roles : user => details.age > 35 ? "Senior" : "Junior"
  }
}
