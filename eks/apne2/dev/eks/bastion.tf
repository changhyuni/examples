resource "aws_instance" "bastion" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  subnet_id     = local.public_subnets[0]
  key_name      = local.keypair_name
  vpc_security_group_ids = [aws_security_group.bastion.id]

  user_data = base64encode(templatefile("${path.module}/templates/bastion.sh.tpl", {
    
  }))

  tags = {
    Name = "bastion"
  }
}

resource "aws_iam_role" "bastion" {
  name = "bastion-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bastion" {
  role       = aws_iam_role.bastion.name
  policy_arn = aws_iam_policy.bastion.arn
}

resource "aws_iam_policy" "bastion" {
  name        = "bastion-policy"
  description = "Allow EKS DescribeCluster action"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowDescribeCluster",
        Effect = "Allow",
        Action = "eks:DescribeCluster",
        Resource = "*"
      }
    ]
  })
}