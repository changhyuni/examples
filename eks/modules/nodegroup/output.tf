output "node_group_arn" {
  description = "노드 그룹의 ARN"
  value       = aws_eks_node_group.nodegroup.arn
}

output "nodegroup_min_node" {
  description = "노드 그룹에 허용되는 최소 노드 수"
  value       = var.nodegroup_min_size
}

output "nodegroup_max_node" {
  description = "노드 그룹에 허용되는 최대 노드 수"
  value       = var.nodegroup_max_size
}

output "nodegroup_desired_node" {
  description = "노드 그룹에 원하는 노드 수"
  value       = var.nodegroup_desired_size
}

output "nodegroup_capacity_type" {
  description = "노드 그룹의 용량 유형 (예: ON_DEMAND, SPOT)"
  value       = var.nodegroup_capacity_type
}

output "nodegroup_instance_types" {
  description = "노드 그룹에 사용되는 인스턴스 타입"
  value       = var.nodegroup_instance_types
}