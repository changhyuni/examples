# resource "aws_security_group" "example" {
#   name   = "example-sg"
#   vpc_id = "vpc-123456"

#   # 인바운드 규칙 1
#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   # 인바운드 규칙 2
#   ingress {
#     from_port   = 443
#     to_port     = 443
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
