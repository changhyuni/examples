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
| [aws_eks_addon.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_addon) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_addons"></a> [addons](#input\_addons) | aws\_eks\_addon 리소스를 관리합니다. | <pre>list(object({<br/>    addon_name           = string<br/>    addon_version        = optional(string, null)<br/>    configuration_values = optional(string, null)<br/>    resolve_conflicts           = optional(string, null)<br/>    resolve_conflicts_on_create = optional(string, null)<br/>    resolve_conflicts_on_update = optional(string, null)<br/>    service_account_role_arn    = optional(string, null)<br/>    create_timeout              = optional(string, null)<br/>    update_timeout              = optional(string, null)<br/>    delete_timeout              = optional(string, null)<br/>  }))</pre> | `[]` | no |
| <a name="input_cluster_name"></a> [cluster\_name](#input\_cluster\_name) | EKS 클러스터 이름 | `string` | n/a | yes |
| <a name="input_enabled"></a> [enabled](#input\_enabled) | 모듈 사용 여부 | `bool` | `true` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | 클러스터에 적용할 태그 맵 | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->