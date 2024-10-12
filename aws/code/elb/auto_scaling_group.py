import boto3
import base64

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

def generate_name(project_name, resource_type):
    return f"{project_name}-{resource_type}"

def create_launch_template(project_name, ami_id, instance_type, key_name, sg_id, user_data):
    lt_name = generate_name(project_name, "lt")
    encoded_user_data = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')
    response = ec2.create_launch_template(
        LaunchTemplateName=lt_name,
        VersionDescription='v1',
        LaunchTemplateData={
            'ImageId': ami_id,
            'InstanceType': instance_type,
            'KeyName': key_name,
            'SecurityGroupIds': [sg_id],
            'UserData': encoded_user_data
        }
    )
    print(f"런치 템플릿 생성됨: {lt_name}")
    return lt_name

def create_auto_scaling_group(project_name, auto_scaling_group_name, launch_template_name, min_size, max_size, subnet_ids, target_group_arns):
    asg_name = generate_name(project_name, auto_scaling_group_name)
    response = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={
            'LaunchTemplateName': launch_template_name,
            'Version': '1'
        },
        MinSize=min_size,
        MaxSize=max_size,
        VPCZoneIdentifier=",".join(subnet_ids),
        TargetGroupARNs=target_group_arns,
        Tags=[
            {
                'ResourceId': asg_name,
                'ResourceType': 'auto-scaling-group',
                'Key': 'Name',
                'Value': asg_name,
                'PropagateAtLaunch': True
            }
        ]
    )
    print(f"오토 스케일링 그룹 생성됨: {asg_name}")
    return asg_name
