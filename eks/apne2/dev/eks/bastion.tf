resource "aws_instance" "bastion" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  subnet_id     = module.vpc.public_subnets[0]
  key_name      = local.keypair_name
  vpc_security_group_ids = [aws_security_group.bastion.id]

  user_data = base64encode(templatefile("${path.module}/templates/bastion.sh.tpl", {
    endpoint               = data.aws_eks_cluster.eks.endpoint
  }))

  
  tags = {
    Name = "${local.name}-bastion"
  }
}