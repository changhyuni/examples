locals {
  launch_template_name = format("%s-%s-%s", var.eks_cluster_name, var.nodegroup_name, "lt")
  ami_owner            = "602401143452"
  ami_base_name        = "amazon-eks-node"
  ami_arch             = "v*"
}

data "aws_eks_cluster" "eks" {
  name = var.eks_cluster_name
}

data "aws_ami" "launch_template_ami" {
  owners      = [local.ami_owner]
  most_recent = true
  filter {
    name   = "name"
    values = [format("%s-%s-%s", local.ami_base_name, data.aws_eks_cluster.eks.version, local.ami_arch)]
  }
}

resource "aws_launch_template" "eks_template" {
  name                   = local.launch_template_name
  key_name               = var.eks_nodes_keypair_name
  image_id               = data.aws_ami.launch_template_ami.image_id
  user_data = base64encode(templatefile("${path.module}/templates/scripts.sh.tpl", {
    endpoint            = data.aws_eks_cluster.eks.endpoint
    cluster_name        = var.eks_cluster_name
    cluster_auth_base64 = data.aws_eks_cluster.eks.certificate_authority[0].data
    kubelet_overrides_json = var.kubelet_overrides_json
  }))
  update_default_version = true

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = var.nodegroup_ebs_volume_size
      volume_type           = var.nodegroup_ebs_volume_type
      delete_on_termination = var.nodegroup_volume_delete_on_termination
      encrypted             = var.nodegroup_ebs_encrypted
    }
  }

  network_interfaces {
    delete_on_termination       = var.nodegroup_network_interfaces_delete_on_termination
  }

  monitoring {
    enabled = var.nodegroup_monitoring_enabled
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(
      {
        Name = format("%s-%s-%s", var.environment, var.nodegroup_name, "eks-node")
      },
      var.tags
    )
  }

  tag_specifications {
    resource_type = "volume"
    tags = merge(
      {
        Name = format("%s-%s-%s", var.environment, var.nodegroup_name, "eks-volume")
      },
      var.tags
    )
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_eks_node_group" "nodegroup" {
  subnet_ids      = var.vpc_subnet_ids
  cluster_name    = var.eks_cluster_name
  node_role_arn   = var.worker_iam_role_arn
  node_group_name = format("%s-%s-%s", var.environment, var.nodegroup_name, "ng")

  scaling_config {
    desired_size = var.nodegroup_desired_size
    max_size     = var.nodegroup_max_size
    min_size     = var.nodegroup_min_size
  }

  labels               = var.k8s_labels
  capacity_type        = var.nodegroup_capacity_type
  instance_types       = var.nodegroup_instance_types
  force_update_version = true

  launch_template {
    id      = aws_launch_template.eks_template.id
    version = aws_launch_template.eks_template.latest_version
  }

  update_config {
    max_unavailable_percentage = 50
  }

  tags = merge(
    {
      Name = format("%s-%s-%s", var.environment, var.nodegroup_name, "ng")
    },
    var.tags
  )
}