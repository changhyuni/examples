data "aws_iam_policy" "SSMManagedInstanceCore" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role" "node_role" {
  name               = "${var.nodegroup_name}-node-role"
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

  tags = merge(
    {
      Name = "${var.nodegroup_name}-node-role"
    },
  )
}

resource "aws_iam_role_policy_attachment" "SSMManagedInstanceCore_attachment" {
  role       = aws_iam_role.node_role.name
  policy_arn = data.aws_iam_policy.SSMManagedInstanceCore.arn
}

resource "aws_iam_policy" "node_autoscaler_policy" {
  name        = "${var.nodegroup_name}-node-autoscaler-policy"
  path        = "/"
  description = "Node auto scaler policy for node groups."
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeTags",
        "autoscaling:SetDesiredCapacity",
        "ec2:DescribeLaunchTemplateVersions",
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "node_autoscaler_policy_attachment" {
  role       = aws_iam_role.node_role.name
  policy_arn = aws_iam_policy.node_autoscaler_policy.arn
}

resource "aws_iam_role_policy_attachment" "worker_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "worker_ecr_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
