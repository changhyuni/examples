output "cluster_name" {
  description = "생성된 EKS 클러스터 이름"
  value       = aws_eks_cluster.this[0].name
}

output "cluster_endpoint" {
  description = "EKS 클러스터 엔드포인트"
  value       = aws_eks_cluster.this[0].endpoint
}

output "cluster_arn" {
  description = "EKS 클러스터 ARN"
  value       = aws_eks_cluster.this[0].arn
}

output "cluster_certificate_authority_data" {
  description = "클러스터 CA 데이터(base64 인코딩)"
  value       = aws_eks_cluster.this[0].certificate_authority[0].data
}

output "eks_cluster_security_group_id" {
  description = "EKS 클러스터 보안 그룹 ID"
  value       = aws_eks_cluster.this[0].vpc_config[0].cluster_security_group_id
}