variable "user_roles" {
  description = "A map of user names and their details including role and age."
  type = map(object({
    role = string
    age  = number
  }))
  default = {
    "june" = {
      role = "Kubernetes Engineer"
      age  = 99
    }
  }
}
