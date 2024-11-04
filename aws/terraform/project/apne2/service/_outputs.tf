# _outputs.tf

output "vpc_id" {
  description = "생성된 VPC의 ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "생성된 퍼블릭 서브넷의 ID 목록"
  value       = [for s in aws_subnet.public : s.id]
}

output "private_subnet_ids" {
  description = "생성된 프라이빗 서브넷의 ID 목록"
  value       = [for s in aws_subnet.private : s.id]
}

output "nat_gateway_id" {
  description = "생성된 NAT 게이트웨이의 ID"
  value       = aws_nat_gateway.nat.id
}

output "ec2_public_ip" {
  description = "EC2 인스턴스의 퍼블릭 IP"
  value       = aws_instance.web.public_ip
}

output "key_pair_name" {
  description = "생성된 키 페어의 이름"
  value       = aws_key_pair.key_pair.key_name
}
