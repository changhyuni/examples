resource "aws_iam_user" "myiam" {
  for_each = var.user_roles

  # 조건에 따라 이름 앞에 "Senior" 추가
  name = each.value.age > 35 ? "Senior-${each.key}" : each.key

  tags = {
    "Role"       = each.value.role
    "UserStatus" = each.value.age > 35 ? "Senior" : "Junior"
  }
}