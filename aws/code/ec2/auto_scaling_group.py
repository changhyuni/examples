import boto3
import base64

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')
cloudwatch = boto3.client('cloudwatch')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def create_launch_template(project_name, ami_id, instance_type, key_name, sg_id, user_data):
    """
    오토 스케일링 그룹에 사용할 런치 템플릿을 생성합니다.
    """
    lt_name = generate_name(project_name, "lt")

    # User data를 base64로 인코딩
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

def create_auto_scaling_group(project_name, auto_scaling_group_name, launch_template_name, min_size, max_size, subnet_ids):
    """
    지정된 런치 템플릿을 사용하여 오토 스케일링 그룹을 생성합니다.
    """
    asg_name = generate_name(project_name, "asg")
    response = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={
            'LaunchTemplateName': launch_template_name,
            'Version': '1'
        },
        MinSize=min_size,
        MaxSize=max_size,
        VPCZoneIdentifier=",".join(subnet_ids),
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

def create_scaling_policy(auto_scaling_group_name, project_name):
    """
    오토 스케일링 그룹에 대한 스케일링 정책을 생성합니다.
    CPU 사용률 10% 이상일 경우 인스턴스를 늘리는 정책을 적용.
    """
    policy_name = generate_name(project_name, "scaling-policy")
    response = autoscaling.put_scaling_policy(
        AutoScalingGroupName=auto_scaling_group_name,
        PolicyName=policy_name,
        PolicyType='TargetTrackingScaling',
        TargetTrackingConfiguration={
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ASGAverageCPUUtilization'
            },
            'TargetValue': 10.0  # CPU 사용률 20% 이상일 때
        }
    )
    scaling_policy_arn = response['PolicyARN']
    print(f"스케일링 정책 생성됨: {policy_name} (ARN: {scaling_policy_arn})")
    return scaling_policy_arn

def create_cpu_alarm(auto_scaling_group_name, project_name, scaling_policy_arn):
    """
    오토 스케일링 그룹에 대한 CloudWatch CPU 알람을 생성합니다.
    스케일링 정책 ARN을 사용하여 CPU 사용량 10% 이상일 때 스케일링 정책을 트리거합니다.
    """
    alarm_name = generate_name(project_name, "cpu-alarm")
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistic='Average',
        Period=30,  # 30초
        EvaluationPeriods=1,
        Threshold=10.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': auto_scaling_group_name
            },
        ],
        AlarmActions=[scaling_policy_arn]  # 스케일링 정책 ARN을 알람 액션으로 추가
    )
    print(f"CPU 사용량 10% 알람 생성됨: {alarm_name}")

