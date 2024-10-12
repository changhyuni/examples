import boto3

ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')

def generate_name(project_name, resource_type, suffix=""):
    """
    프로젝트 이름과 리소스 타입, 그리고 선택적인 접미사를 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}{suffix}"

def create_target_group(project_name, vpc_id, suffix):
    """
    지정된 VPC에 타겟 그룹을 생성합니다.
    """
    target_group_name = generate_name(project_name, "tg", suffix)
    response = elbv2.create_target_group(
        Name=target_group_name,
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        TargetType='instance',
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2,
        Matcher={'HttpCode': '200'}
    )
    target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
    print(f"타겟 그룹 생성됨: {target_group_name} (ARN: {target_group_arn})")
    return target_group_arn

def create_load_balancer(project_name, subnets, security_groups):
    """
    ALB를 생성합니다.
    """
    lb_name = generate_name(project_name, "alb")
    response = elbv2.create_load_balancer(
        Name=lb_name,
        Subnets=subnets,
        SecurityGroups=security_groups,
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4',
        Tags=[{'Key': 'Name', 'Value': lb_name}]
    )
    lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    print(f"로드 밸런서 생성됨: {lb_name} (ARN: {lb_arn})")
    return lb_arn

def create_listener(project_name, lb_arn, target_group_arns):
    """
    ALB에 리스너를 생성하고 두 개의 타겟 그룹으로 트래픽을 분산합니다.
    """
    listener_name = generate_name(project_name, "listener")
    response = elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'ForwardConfig': {
                    'TargetGroups': [
                        {'TargetGroupArn': target_group_arns[0], 'Weight': 1},
                        {'TargetGroupArn': target_group_arns[1], 'Weight': 1}
                    ]
                }
            }
        ]
    )
    listener_arn = response['Listeners'][0]['ListenerArn']
    print(f"리스너 생성됨: (ARN: {listener_arn})")
    return listener_arn
