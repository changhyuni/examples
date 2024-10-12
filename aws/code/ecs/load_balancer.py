import boto3

ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')

def generate_name(project_name, resource_type, suffix=""):
    """
    프로젝트 이름과 리소스 타입, 그리고 선택적인 접미사를 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}{suffix}"

def create_target_group(project_name, vpc_id, suffix, launch_type='FARGATE'):
    """
    타겟 그룹을 생성합니다.
    launch_type에 따라 target_type을 설정합니다.
    """
    target_group_name = f"{project_name}-tg-{suffix}"
    
    # 런치 타입에 따라 target_type 설정
    if launch_type == 'FARGATE':
        target_type = 'ip'
    elif launch_type == 'EC2':
        target_type = 'instance'
    else:
        raise ValueError("Unsupported launch type. Choose 'FARGATE' or 'EC2'.")
    
    try:
        response = elbv2.create_target_group(
            Name=target_group_name,
            Protocol='HTTP',
            Port=80,
            VpcId=vpc_id,
            TargetType=target_type,  # 타겟 타입 설정
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
    except elbv2.exceptions.AlreadyExistsException:
        response = elbv2.describe_target_groups(
            Names=[target_group_name]
        )
        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        print(f"이미 존재하는 타겟 그룹 사용: {target_group_name} (ARN: {target_group_arn})")
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
    ALB에 리스너와 기본 규칙을 생성합니다.
    target_group_arns: 타겟 그룹 ARN의 리스트 (None 값 제외)
    """
    listener_name = generate_name(project_name, "listener")
    valid_target_group_arns = [arn for arn in target_group_arns if arn is not None]
    response = elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'ForwardConfig': {
                    'TargetGroups': [
                        {'TargetGroupArn': target_group_arns[0], 'Weight': 1}
                    ]
                }
            }
        ]
    )
    listener_arn = response['Listeners'][0]['ListenerArn']
    print(f"리스너 생성됨: (ARN: {listener_arn})")
    return listener_arn
