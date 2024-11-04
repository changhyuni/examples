terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
        source  = "hashicorp/aws"
        version = "~> 3.0"
    }
  }
}

provider "aws" {
  region  = "ap-northeast-2"
}

resource "aws_vpc" "vpc" {
    cidr_block = "192.168.0.0/24"
    tags = {
        Name = "workflow"
    }
}
