# terraform.tfvars

aws_region = "ap-northeast-2"  # 원하는 리전으로 변경

vpc_cidr_block = "10.0.0.0/16"

public_subnet_cidr_blocks = {
  "public-1" = "10.0.1.0/24"
  "public-2" = "10.0.2.0/24"
}

private_subnet_cidr_blocks = {
  "private-1" = "10.0.3.0/24"
  "private-2" = "10.0.4.0/24"
}

instance_type = "t2.micro"

ami_id = ""  # 특정 AMI를 사용하려면 AMI ID 입력

key_pair_name   = "key" 
public_key_path = "./"      

ingress_rules = [
  {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # SSH 접근을 허용할 IP 대역 (내 아이피 꼭 넣어주세요)
  }
]