resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# AWS에 키 페어 등록
resource "aws_key_pair" "key_pair" {
  key_name   = local.keypair_name
  public_key = tls_private_key.key.public_key_openssh
}

# 로컬 파일 시스템에 비공개 키 저장
resource "local_file" "key" {
  filename        = "./${local.keypair_name}.pem"   
  content         = tls_private_key.key.private_key_pem
  file_permission = "0600"
}