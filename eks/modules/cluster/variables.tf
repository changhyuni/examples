variable "enabled" {
  description = "모듈 사용 여부"
  type        = bool
  default     = true
}

variable "cluster_name" {
  description = "EKS 클러스터 이름"
  type        = string
}

variable "cluster_version" {
  description = "EKS 클러스터 쿠버네티스 버전"
  type        = string
  default     = "1.27"
}

variable "subnet_ids" {
  description = "EKS 클러스터에 사용할 Subnet ID 리스트"
  type        = list(string)
}

variable "endpoint_public_access" {
  description = "EKS 클러스터 Public Access 활성화 여부"
  type        = bool
  default     = true
}

variable "endpoint_private_access" {
  description = "EKS 클러스터 Private Access 활성화 여부"
  type        = bool
  default     = false
}

variable "public_access_cidrs" {
  description = "Public endpoint 접근을 허용할 CIDR 블록 리스트"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "security_group_ids" {
  description = "클러스터에 연결할 보안 그룹들(옵션)"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "클러스터에 적용할 태그 맵"
  type        = map(string)
  default     = {}
}


variable "enabled_cluster_log_types" {
  type        = list(string)
  description = "활성화할 원하는 제어 평면 로깅의 목록입니다."
  default     = []
}


variable "access_config" {
  type = object({
    authentication_mode                         = optional(string, "API")
    bootstrap_cluster_creator_admin_permissions = optional(bool, false)
  })
  description = "EKS 클러스터 접근 설정입니다."
  default     = {}
  nullable    = false

  validation {
    condition     = !contains(["CONFIG_MAP"], var.access_config.authentication_mode)
    error_message = "CONFIG_MAP authentication_mode은 지원되지 않습니다."
  }
}

variable "access_entry_map" {
  type = map(object({
    user_name                = optional(string)
    kubernetes_groups        = optional(list(string), [])
    type                     = optional(string, "STANDARD")
    access_policy_associations = optional(map(object({
      access_scope = optional(object({
        type       = optional(string, "cluster")
        namespaces = optional(list(string))
      }), {})
    })), {})
  }))
  description = "EKS 클러스터에 접근할 IAM Principal과 그에 대한 권한을 정의하는 맵입니다."
  default     = {}
  nullable    = false
}

variable "access_entries" {
  type = list(object({
    principal_arn     = string
    user_name         = optional(string, null)
    kubernetes_groups = optional(list(string), null)
  }))
  description = "EKS 클러스터에 접근할 IAM Principal의 리스트입니다."
  default     = []
  nullable    = false
}

variable "allowed_security_group_ids" {
  type        = list(string)
  default     = []
  description = "클러스터에 접근을 허용할 보안 그룹 ID 리스트입니다."
}

variable "allowed_cidr_blocks" {
  type        = list(string)
  default     = []
  description = "클러스터에 접근을 허용할 IPv4 CIDR 블록 리스트입니다."
}

variable "service_ipv4_cidr" {
  type        = string
  description = "EKS 클러스터의 서비스 IP 범위입니다."
  default     = "172.20.0.0/16"
}