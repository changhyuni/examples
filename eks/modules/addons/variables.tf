variable "enabled" {
  description = "모듈 사용 여부"
  type        = bool
  default     = true
}

variable "tags" {
  description = "클러스터에 적용할 태그 맵"
  type        = map(string)
  default     = {}
}

variable "addons" {
  type = list(object({
    addon_name           = string
    addon_version        = optional(string, null)
    configuration_values = optional(string, null)
    resolve_conflicts           = optional(string, null)
    resolve_conflicts_on_create = optional(string, null)
    resolve_conflicts_on_update = optional(string, null)
    service_account_role_arn    = optional(string, null)
    create_timeout              = optional(string, null)
    update_timeout              = optional(string, null)
    delete_timeout              = optional(string, null)
  }))
  description = "aws_eks_addon 리소스를 관리합니다."
  default     = []
}

variable "cluster_name" {
  description = "EKS 클러스터 이름"
  type        = string
}