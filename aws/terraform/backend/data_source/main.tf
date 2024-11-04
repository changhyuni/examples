terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      # version = "5.61.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

data "aws_vpc" "example" {
  default = true
}

data "aws_ami" "ami_ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_subnet" "example" {
  vpc_id            = data.aws_vpc.example.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-northeast-2"
}

resource "aws_instance" "ec2" { 
  ami           = data.aws_ami.ami_ubuntu.id
  instance_type = "t2.micro"
}