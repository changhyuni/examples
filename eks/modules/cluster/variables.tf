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

variable "cluster_log_retention_period" {
  type        = number
  description = "클러스터 로그를 보존할 일수입니다."
  default     = 0
}

variable "permissions_boundary" {
  type        = string
  description = "제공된 경우, 모든 IAM 역할은 이 권한 경계가 첨부된 상태로 생성됩니다."
  default     = null
}

variable "cloudwatch_log_group_class" {
  type        = string
  description = "로그 그룹의 로그 클래스를 지정합니다."
  default     = null
}


variable "upgrade_policy" {
  type = object({
    support_type = optional(string, null)
  })
  description = "클러스터에 사용할 지원 정책의 구성 블록입니다."
  default     = null
}

variable "cluster_attributes" {
  type        = list(string)
  description = "레이블 모듈의 기본 클러스터 속성을 재정의합니다."
  default     = ["cluster"]
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

variable "access_policy_associations" {
  type = list(object({
    principal_arn = string
    policy_arn    = string
    access_scope = object({
      type       = optional(string, "cluster")
      namespaces = optional(list(string))
    })
  }))
  description = "EKS 클러스터에 IAM 정책을 연관짓기 위한 설정입니다."
  default     = []
  nullable    = false
}

variable "access_entries_for_nodes" {
  type        = map(list(string))
  default     = {}
  nullable    = false
  description = "비관리형 워커 노드를 위한 IAM 역할 목록입니다."

  validation {
    condition     = length([for k in keys(var.access_entries_for_nodes) : k if !contains(["EC2_LINUX", "EC2_WINDOWS"], k)]) == 0
    error_message = "access_entries_for_nodes는 EC2_LINUX 및 EC2_WINDOWS 키만 허용합니다."
  }

  validation {
    condition     = !(contains(keys(var.access_entries_for_nodes), "FARGATE_LINUX"))
    error_message = "FARGATE_LINUX는 지원되지 않습니다."
  }
}

variable "managed_security_group_rules_enabled" {
  type        = bool
  description = "EKS 관리 보안 그룹의 인그레스 및 이그레스 규칙을 활성화/비활성화하는 플래그입니다."
  default     = true
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

variable "custom_ingress_rules" {
  type = list(object({
    description              = string
    from_port                = number
    to_port                  = number
    protocol                 = string
    source_security_group_id = string
  }))
  description = "커스텀 보안 그룹 인그레스 규칙의 리스트입니다."
  default     = []
}

variable "service_ipv4_cidr" {
  type        = string
  description = "EKS 클러스터의 서비스 IP 범위입니다."
  default     = "172.20.0.0/16"
}