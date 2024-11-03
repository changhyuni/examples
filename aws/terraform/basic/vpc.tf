# Terraform Settings
terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Provider
provider "aws" {
  region = var.aws_region
}

# Locals
locals {
  default_tags = {
    Project     = "basic"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
  cidr = "${var.base_cidr_block}/24"
}

# Resource 
resource "aws_vpc" "project1vpc" {
  cidr_block = local.cidr
  tags       = merge(local.default_tags, { Name = var.vpc_name })
}

# Variables
variable "aws_region" {
  type        = string
  description = "AWS region for deploying resources"
  default     = "ap-northeast-2"
}

variable "base_cidr_block" {
  type        = string
  description = "Base CIDR block for the VPC"
  default     = "192.168.0.0"
}

variable "vpc_name" {
  type        = string
  description = "Name tag for the VPC"
  default     = "basic"
}

variable "environment" {
  type        = string
  description = "DeploymTent environment (e.g., dev, prod)"
  default     = "development"
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of 'development', 'staging', or 'production'."
  }
}

# Outputs
output "vpc_id" {
  description = "The ID of the created VPC"
  value       = aws_vpc.project1vpc.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the created VPC"
  value       = aws_vpc.project1vpc.cidr_block
}