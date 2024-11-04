data "terraform_remote_state" "project_a" {
  backend = "local"
  config = {
    path = "../a/terraform.tfstate"
  }
}

output "iam_user_name_from_project_a" {
  value = data.terraform_remote_state.project_a.outputs.iam_user_name
}

output "iam_user_arn_from_project_a" {
  value = data.terraform_remote_state.project_a.outputs.iam_user_arn
}
