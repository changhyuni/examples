provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_iam_user" "example" {
  name = "june-remote-state"
}

output "iam_user_name" {
  value = aws_iam_user.example.name
}

output "iam_user_arn" {
  value = aws_iam_user.example.arn
}
