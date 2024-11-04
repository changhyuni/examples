output "user_age" {
  description = "A map of users and their status (Senior/Junior) based on age."
  value = {
    for user, details in var.user_roles : user => details.age > 35 ? "Senior" : "Junior"
  }
}
