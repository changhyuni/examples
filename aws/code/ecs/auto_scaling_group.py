# ec2_launch_template.py
import boto3

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

def create_launch_template(template_name, ami_id, instance_type, security_group_ids, key_name, iam_instance_profile_name, user_data):
    try:
        response = ec2.create_launch_template(
            LaunchTemplateName=template_name,
            LaunchTemplateData={
                'ImageId': ami_id,
                'InstanceType': instance_type,
                'SecurityGroupIds': security_group_ids,
                'KeyName': key_name,
                'IamInstanceProfile': {
                    'Name': iam_instance_profile_name
                },
                'UserData': user_data
            }
        )
        print(f"Launch Template 생성됨: {template_name}")
    except ec2.exceptions.ClientError as e:
        if 'InvalidLaunchTemplateName.AlreadyExistsException' in str(e):
            print(f"이미 존재하는 Launch Template 사용: {template_name}")
        else:
            print(f"Launch Template 생성 오류: {e}")
            raise e
    return template_name

def create_auto_scaling_group(asg_name, launch_template_name, min_size, max_size, subnet_ids, target_group_arns):
    try:
        response = autoscaling.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchTemplate={
                'LaunchTemplateName': launch_template_name
            },
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=min_size,
            VPCZoneIdentifier=",".join(subnet_ids),
            TargetGroupARNs=target_group_arns,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': asg_name,
                    'PropagateAtLaunch': True
                }
            ]
        )
        print(f"Auto Scaling Group 생성됨: {asg_name}")
    except autoscaling.exceptions.AlreadyExistsFault:
        print(f"이미 존재하는 Auto Scaling Group 사용: {asg_name}")
    except Exception as e:
        print(f"Auto Scaling Group 생성 오류: {e}")
        raise e
    return asg_name
