resource "aws_security_group" "public_node" {
  name        = "${local.name}-public-node-sg"
  description = "Public Node Security Group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.my_ip]
    description = "Allow SSH traffic from admin PC"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.environment}-public-node-sg"
  }
}

resource "aws_security_group" "private_node" {
  name        = "${local.name}-private-node-sg"
  description = "Private Node Security Group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [aws_security_group.bastion.id]
    description = "Allow SSH traffic from bastion"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.environment}-private-node-sg"
  }

  depends_on = [
    aws_security_group.bastion
  ]
}

resource "aws_security_group" "cluster_private_access" {
  name        = "${local.name}-cluster-private-access-sg"
  description = "Cluster Private Security Group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.bastion.id]
    description = "Allow K8s API traffic from private bastion"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.environment}-cluster-private-access-sg"
  }

  depends_on = [
    aws_security_group.bastion
  ]
}

resource "aws_security_group" "bastion" {
  name        = "${local.name}-bastion-sg"
  description = "Bastion Security Group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.my_ip]
    description = "Allow SSH traffic from admin PC"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.environment}-bastion-sg"
  }
}