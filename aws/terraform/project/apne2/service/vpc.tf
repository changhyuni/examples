# vpc.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${local.project}-vpc"
  }
}

resource "aws_subnet" "public" {
  for_each = var.public_subnet_cidr_blocks

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  map_public_ip_on_launch = true
  availability_zone = element(local.azs, index(keys(var.public_subnet_cidr_blocks), each.key))

  tags = {
    Name = "${local.project}-public-subnet-${each.key}"
  }
}

resource "aws_subnet" "private" {
  for_each = var.private_subnet_cidr_blocks

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  map_public_ip_on_launch = false
  availability_zone = element(local.azs, index(keys(var.private_subnet_cidr_blocks), each.key))

  tags = {
    Name = "${local.project}-private-subnet-${each.key}"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project}-igw"
  }
}

resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "${local.project}-eip-nat"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public["public-1"].id  # 첫 번째 퍼블릭 서브넷에 NAT 게이트웨이 생성

  depends_on = [aws_internet_gateway.igw]

  tags = {
    Name = "${local.project}-nat-gateway"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${local.project}-public-route-table"
  }
}

resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "${local.project}-private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}
