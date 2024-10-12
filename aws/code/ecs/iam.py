# iam_roles.py
import boto3
import json

iam = boto3.client('iam')

def create_ecs_instance_role(project_name):
    """
    ECS 인스턴스 역할을 생성하고 정책을 연결합니다.
    """
    role_name = f"{project_name}-ecs-instance-role"
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            }),
            Description="Role for ECS EC2 instances"
        )
        role_arn = response['Role']['Arn']
        print(f"ECS 인스턴스 역할 생성됨: {role_name} (ARN: {role_arn})")
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        print(f"이미 존재하는 ECS 인스턴스 역할 사용: {role_name} (ARN: {role_arn})")
    
    # 정책 연결
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
    print(f"정책 {policy_arn}이(가) 역할 {role_name}에 연결되었습니다.")
    
    return role_name

def create_task_role(project_name):
    """
    ECS 태스크 역할을 생성합니다.
    """
    role_name = f"{project_name}-task-role"
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            }),
            Description="Role for ECS tasks"
        )
        role_arn = response['Role']['Arn']
        print(f"ECS 태스크 역할 생성됨: {role_name} (ARN: {role_arn})")
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        print(f"이미 존재하는 ECS 태스크 역할 사용: {role_name} (ARN: {role_arn})")
    
    # 필요한 정책 연결
    policies = [
        "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",  # 필요 시 추가
    ]
    for policy_arn in policies:
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f"정책 {policy_arn}이(가) 역할 {role_name}에 연결되었습니다.")
    
    return role_arn

def create_execution_role(project_name):
    """
    ECS 작업 실행 역할(Task Execution Role)을 생성하고 정책을 연결합니다.
    """
    role_name = f"{project_name}-execution-role"
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description="ECS Task Execution Role for pulling images and logs"
        )
        role_arn = response['Role']['Arn']
        print(f"작업 실행 역할 생성됨: {role_name} (ARN: {role_arn})")
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        print(f"이미 존재하는 작업 실행 역할 사용: {role_name} (ARN: {role_arn})")
    
    # 필요한 정책 연결
    policies = [
        "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
        "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"  # 필요 시 추가
    ]
    for policy_arn in policies:
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f"정책 {policy_arn}이(가) 역할 {role_name}에 연결되었습니다.")
    
    return role_arn

def create_ecs_instance_profile(project_name, role_name):
    instance_profile_name = f"{project_name}-ecs-instance-profile"
    try:
        iam.create_instance_profile(
            InstanceProfileName=instance_profile_name
        )
        print(f"IAM 인스턴스 프로파일 생성됨: {instance_profile_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"이미 존재하는 IAM 인스턴스 프로파일 사용: {instance_profile_name}")
    except Exception as e:
        print(f"IAM 인스턴스 프로파일 생성 오류: {e}")
        raise e

    # 역할을 인스턴스 프로파일에 연결
    try:
        iam.add_role_to_instance_profile(
            InstanceProfileName=instance_profile_name,
            RoleName=role_name
        )
        print(f"역할 {role_name}이 인스턴스 프로파일 {instance_profile_name}에 연결되었습니다.")
    except iam.exceptions.LimitExceededException:
        print(f"인스턴스 프로파일 {instance_profile_name}에 이미 역할이 연결되어 있습니다.")
    except Exception as e:
        print(f"역할 연결 오류: {e}")
        raise e

    return instance_profile_name