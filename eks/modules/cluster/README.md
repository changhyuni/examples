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
| [aws_eks_access_entry.map](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_access_entry) | resource |
| [aws_eks_access_policy_association.map](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_access_policy_association) | resource |
| [aws_eks_cluster.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_cluster) | resource |
| [aws_iam_role.eks_cluster_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.eks_cluster_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.eks_service_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_access_config"></a> [access\_config](#input\_access\_config) | EKS 클러스터 접근 설정입니다. | <pre>object({<br/>    authentication_mode                         = optional(string, "API")<br/>    bootstrap_cluster_creator_admin_permissions = optional(bool, false)<br/>  })</pre> | `{}` | no |
| <a name="input_access_entries"></a> [access\_entries](#input\_access\_entries) | EKS 클러스터에 접근할 IAM Principal의 리스트입니다. | <pre>list(object({<br/>    principal_arn     = string<br/>    user_name         = optional(string, null)<br/>    kubernetes_groups = optional(list(string), null)<br/>  }))</pre> | `[]` | no |
| <a name="input_access_entry_map"></a> [access\_entry\_map](#input\_access\_entry\_map) | EKS 클러스터에 접근할 IAM Principal과 그에 대한 권한을 정의하는 맵입니다. | <pre>map(object({<br/>    user_name                = optional(string)<br/>    kubernetes_groups        = optional(list(string), [])<br/>    type                     = optional(string, "STANDARD")<br/>    access_policy_associations = optional(map(object({<br/>      access_scope = optional(object({<br/>        type       = optional(string, "cluster")<br/>        namespaces = optional(list(string))<br/>      }), {})<br/>    })), {})<br/>  }))</pre> | `{}` | no |
| <a name="input_allowed_cidr_blocks"></a> [allowed\_cidr\_blocks](#input\_allowed\_cidr\_blocks) | 클러스터에 접근을 허용할 IPv4 CIDR 블록 리스트입니다. | `list(string)` | `[]` | no |
| <a name="input_allowed_security_group_ids"></a> [allowed\_security\_group\_ids](#input\_allowed\_security\_group\_ids) | 클러스터에 접근을 허용할 보안 그룹 ID 리스트입니다. | `list(string)` | `[]` | no |
| <a name="input_cluster_name"></a> [cluster\_name](#input\_cluster\_name) | EKS 클러스터 이름 | `string` | n/a | yes |
| <a name="input_cluster_version"></a> [cluster\_version](#input\_cluster\_version) | EKS 클러스터 쿠버네티스 버전 | `string` | `"1.27"` | no |
| <a name="input_enabled"></a> [enabled](#input\_enabled) | 모듈 사용 여부 | `bool` | `true` | no |
| <a name="input_enabled_cluster_log_types"></a> [enabled\_cluster\_log\_types](#input\_enabled\_cluster\_log\_types) | 활성화할 원하는 제어 평면 로깅의 목록입니다. | `list(string)` | `[]` | no |
| <a name="input_endpoint_private_access"></a> [endpoint\_private\_access](#input\_endpoint\_private\_access) | EKS 클러스터 Private Access 활성화 여부 | `bool` | `false` | no |
| <a name="input_endpoint_public_access"></a> [endpoint\_public\_access](#input\_endpoint\_public\_access) | EKS 클러스터 Public Access 활성화 여부 | `bool` | `true` | no |
| <a name="input_public_access_cidrs"></a> [public\_access\_cidrs](#input\_public\_access\_cidrs) | Public endpoint 접근을 허용할 CIDR 블록 리스트 | `list(string)` | <pre>[<br/>  "0.0.0.0/0"<br/>]</pre> | no |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | 클러스터에 연결할 보안 그룹들(옵션) | `list(string)` | `[]` | no |
| <a name="input_service_ipv4_cidr"></a> [service\_ipv4\_cidr](#input\_service\_ipv4\_cidr) | EKS 클러스터의 서비스 IP 범위입니다. | `string` | `"172.20.0.0/16"` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | EKS 클러스터에 사용할 Subnet ID 리스트 | `list(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | 클러스터에 적용할 태그 맵 | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cluster_arn"></a> [cluster\_arn](#output\_cluster\_arn) | EKS 클러스터 ARN |
| <a name="output_cluster_certificate_authority_data"></a> [cluster\_certificate\_authority\_data](#output\_cluster\_certificate\_authority\_data) | 클러스터 CA 데이터(base64 인코딩) |
| <a name="output_cluster_endpoint"></a> [cluster\_endpoint](#output\_cluster\_endpoint) | EKS 클러스터 엔드포인트 |
| <a name="output_cluster_name"></a> [cluster\_name](#output\_cluster\_name) | 생성된 EKS 클러스터 이름 |
| <a name="output_eks_cluster_security_group_id"></a> [eks\_cluster\_security\_group\_id](#output\_eks\_cluster\_security\_group\_id) | EKS 클러스터 보안 그룹 ID |
<!-- END_TF_DOCS -->