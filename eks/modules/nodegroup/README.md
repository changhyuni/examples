<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_eks_node_group.nodegroup](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_node_group) | resource |
| [aws_iam_policy.node_autoscaler_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.node_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.SSMManagedInstanceCore_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.cni_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.node_autoscaler_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.worker_ecr_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.worker_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_launch_template.eks_template](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/launch_template) | resource |
| [aws_ami.launch_template_ami](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ami) | data source |
| [aws_eks_cluster.eks](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/eks_cluster) | data source |
| [aws_iam_policy.SSMManagedInstanceCore](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_eks_cluster_name"></a> [eks\_cluster\_name](#input\_eks\_cluster\_name) | EKS 클러스터 이름 | `string` | n/a | yes |
| <a name="input_eks_nodes_keypair_name"></a> [eks\_nodes\_keypair\_name](#input\_eks\_nodes\_keypair\_name) | EKS 클러스터 노드에 사용할 키페어 이름 | `string` | `""` | no |
| <a name="input_k8s_labels"></a> [k8s\_labels](#input\_k8s\_labels) | 노드 그룹에 적용할 k8s 라벨 | `map(any)` | `{}` | no |
| <a name="input_kubelet_overrides_json"></a> [kubelet\_overrides\_json](#input\_kubelet\_overrides\_json) | kubelet 설정 오버라이드 JSON 문자열 | `string` | `"{}"` | no |
| <a name="input_node_security_group_ids"></a> [node\_security\_group\_ids](#input\_node\_security\_group\_ids) | 노드 보안 그룹 ID | `list(string)` | n/a | yes |
| <a name="input_nodegroup_capacity_type"></a> [nodegroup\_capacity\_type](#input\_nodegroup\_capacity\_type) | 노드 그룹 용량 유형(ON\_DEMAND 또는 SPOT) | `string` | `"ON_DEMAND"` | no |
| <a name="input_nodegroup_desired_size"></a> [nodegroup\_desired\_size](#input\_nodegroup\_desired\_size) | 노드 그룹 원하는 노드 수 | `number` | `3` | no |
| <a name="input_nodegroup_ebs_encrypted"></a> [nodegroup\_ebs\_encrypted](#input\_nodegroup\_ebs\_encrypted) | EBS 볼륨 암호화 여부 | `bool` | `true` | no |
| <a name="input_nodegroup_ebs_volume_size"></a> [nodegroup\_ebs\_volume\_size](#input\_nodegroup\_ebs\_volume\_size) | 노드 그룹 노드에 할당할 EBS 볼륨 크기 (GB) | `number` | `50` | no |
| <a name="input_nodegroup_ebs_volume_type"></a> [nodegroup\_ebs\_volume\_type](#input\_nodegroup\_ebs\_volume\_type) | EBS 볼륨 타입 | `string` | `"gp3"` | no |
| <a name="input_nodegroup_instance_types"></a> [nodegroup\_instance\_types](#input\_nodegroup\_instance\_types) | 노드 그룹에 사용할 인스턴스 타입 | `list(string)` | <pre>[<br/>  "t2.micro"<br/>]</pre> | no |
| <a name="input_nodegroup_max_size"></a> [nodegroup\_max\_size](#input\_nodegroup\_max\_size) | 노드 그룹 최대 노드 수 | `number` | `3` | no |
| <a name="input_nodegroup_min_size"></a> [nodegroup\_min\_size](#input\_nodegroup\_min\_size) | 노드 그룹 최소 노드 수 | `number` | `1` | no |
| <a name="input_nodegroup_monitoring_enabled"></a> [nodegroup\_monitoring\_enabled](#input\_nodegroup\_monitoring\_enabled) | 노드그룹 모니터링 활성화 여부 | `bool` | `true` | no |
| <a name="input_nodegroup_name"></a> [nodegroup\_name](#input\_nodegroup\_name) | EKS 노드 그룹의 이름 | `string` | n/a | yes |
| <a name="input_nodegroup_network_interfaces_delete_on_termination"></a> [nodegroup\_network\_interfaces\_delete\_on\_termination](#input\_nodegroup\_network\_interfaces\_delete\_on\_termination) | 인스턴스 종료시 네트워크 인터페이스 삭제 여부 | `bool` | `true` | no |
| <a name="input_nodegroup_volume_delete_on_termination"></a> [nodegroup\_volume\_delete\_on\_termination](#input\_nodegroup\_volume\_delete\_on\_termination) | 인스턴스 종료시 볼륨 삭제 여부 | `bool` | `true` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | 공통 태그 | `map(string)` | `{}` | no |
| <a name="input_vpc_subnet_ids"></a> [vpc\_subnet\_ids](#input\_vpc\_subnet\_ids) | VPC 서브넷 ID 목록 | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_node_group_arn"></a> [node\_group\_arn](#output\_node\_group\_arn) | 노드 그룹의 ARN |
| <a name="output_nodegroup_capacity_type"></a> [nodegroup\_capacity\_type](#output\_nodegroup\_capacity\_type) | 노드 그룹의 용량 유형 (예: ON\_DEMAND, SPOT) |
| <a name="output_nodegroup_desired_node"></a> [nodegroup\_desired\_node](#output\_nodegroup\_desired\_node) | 노드 그룹에 원하는 노드 수 |
| <a name="output_nodegroup_instance_types"></a> [nodegroup\_instance\_types](#output\_nodegroup\_instance\_types) | 노드 그룹에 사용되는 인스턴스 타입 |
| <a name="output_nodegroup_max_node"></a> [nodegroup\_max\_node](#output\_nodegroup\_max\_node) | 노드 그룹에 허용되는 최대 노드 수 |
| <a name="output_nodegroup_min_node"></a> [nodegroup\_min\_node](#output\_nodegroup\_min\_node) | 노드 그룹에 허용되는 최소 노드 수 |
<!-- END_TF_DOCS -->