# _variables.tf

variable "aws_region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"
}

variable "vpc_cidr_block" {
  description = "VPC의 CIDR 블록"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr_blocks" {
  description = "퍼블릭 서브넷의 CIDR 블록 리스트"
  type        = map(string)
  default     = {
    "public-1" = "10.0.1.0/24"
    "public-2" = "10.0.2.0/24"
  }
}

variable "private_subnet_cidr_blocks" {
  description = "프라이빗 서브넷의 CIDR 블록 리스트"
  type        = map(string)
  default     = {
    "private-1" = "10.0.3.0/24"
    "private-2" = "10.0.4.0/24"
  }
}

variable "instance_type" {
  description = "EC2 인스턴스 타입"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "EC2 인스턴스에 사용할 AMI ID"
  type        = string
  default     = ""  # 원하는 AMI ID로 변경
}

variable "key_pair_name" {
  description = "생성할 키 페어의 이름"
  type        = string
  default     = "terraform-key-pair"
}

variable "public_key_path" {
  description = "로컬에 있는 공개 키 파일의 경로"
  type        = string
  default     = "~/.ssh/id_rsa.pub"  # 로컬 공개 키 파일 경로로 변경
}

variable "ingress_rules" {
  description = "보안 그룹의 인바운드 규칙 목록"
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
    {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}
