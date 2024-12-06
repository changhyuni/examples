variable "environment" {
  description = "환경명 (예: dev, prod)"
  type        = string
}

variable "name" {
  description = "리소스 기본 이름"
  type        = string
}

variable "eks_cluster_name" {
  description = "EKS 클러스터 이름"
  type        = string
}

variable "eks_nodes_keypair_name" {
  description = "EKS 클러스터 노드에 사용할 키페어 이름"
  type        = string
  default     = ""
}

variable "nodegroup_name" {
  description = "EKS 노드 그룹의 이름"
  type        = string
}

variable "nodegroup_instance_types" {
  description = "노드 그룹에 사용할 인스턴스 타입"
  type        = list(string)
  default     = ["t3a.medium"]
}

variable "nodegroup_capacity_type" {
  description = "노드 그룹 용량 유형(ON_DEMAND 또는 SPOT)"
  type        = string
  default     = "ON_DEMAND"
}

variable "nodegroup_min_size" {
  description = "노드 그룹 최소 노드 수"
  type        = number
  default     = 1
}

variable "nodegroup_max_size" {
  description = "노드 그룹 최대 노드 수"
  type        = number
  default     = 3
}

variable "nodegroup_desired_size" {
  description = "노드 그룹 원하는 노드 수"
  type        = number
  default     = 3
}

variable "nodegroup_ebs_volume_size" {
  description = "노드 그룹 노드에 할당할 EBS 볼륨 크기 (GB)"
  type        = number
  default     = 50
}

variable "nodegroup_ebs_volume_type" {
  description = "EBS 볼륨 타입"
  type        = string
  default     = "gp3"
}

variable "nodegroup_ebs_encrypted" {
  description = "EBS 볼륨 암호화 여부"
  type        = bool
  default     = true
}

variable "vpc_subnet_ids" {
  description = "VPC 서브넷 ID 목록"
  type        = list(string)
}

variable "tags" {
  description = "공통 태그"
  type        = map(string)
  default     = {}
}

variable "k8s_labels" {
  description = "노드 그룹에 적용할 k8s 라벨"
  type        = map(any)
  default     = {}
}

variable "worker_iam_role_arn" {
  description = "워커 노드용 IAM Role ARN (외부에서 주입할 경우)"
  type        = string
  default     = ""
}

variable "nodegroup_network_interfaces_delete_on_termination" {
  description = "인스턴스 종료시 네트워크 인터페이스 삭제 여부"
  type        = bool
  default     = true
}

variable "nodegroup_volume_delete_on_termination" {
  description = "인스턴스 종료시 볼륨 삭제 여부"
  type        = bool
  default     = true
}

variable "nodegroup_volume_delete_on_termination" {
  description = "인스턴스 종료시 볼륨 삭제 여부"
  type        = bool
  default     = true
}

variable "nodegroup_monitoring_enabled" {
  description = "노드그룹 모니터링 활성화 여부"
  type        = bool
  default     = true
}

variable "kubelet_overrides_json" {
  description = "kubelet 설정 오버라이드 JSON 문자열"
  type        = string
  default     = "{}"
}
