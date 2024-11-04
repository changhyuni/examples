module "this" {
  source = "./iam"

  user_roles = {
    "alice" = {
      role = "DevOps Engineer"
      age  = 36
    }
    "bob" = {
      role = "System Engineer"
      age  = 29
    }
  }
}

output "user_status" {
  value       = module.this.user_age
}