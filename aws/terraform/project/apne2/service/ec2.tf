# ec2.tf

# 키 페어 생성
resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# AWS에 키 페어 등록
resource "aws_key_pair" "key_pair" {
  key_name   = var.key_pair_name
  public_key = tls_private_key.key.public_key_openssh

  tags = {
    Name = "${local.project}-key-pair"
  }
}

# 로컬 파일 시스템에 비공개 키 저장
resource "local_file" "key" {
  filename        = "./${var.key_pair_name}.pem"
  content         = tls_private_key.key.private_key_pem
  file_permission = "0600"
}

resource "aws_security_group" "ec2_sg" {
  name        = "${local.project}-ec2-sg"
  description = "ec2"
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      description = ingress.value.description
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    description = "outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.project}-ec2-sg"
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public["public-1"].id  # 첫 번째 퍼블릭 서브넷에 인스턴스 생성
  key_name      = aws_key_pair.key_pair.key_name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "${local.project}-ec2"
  }
}
