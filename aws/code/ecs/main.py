import base64
import time
from vpc.vpc import create_vpc
from vpc.subnet import create_subnet
from vpc.internet_gateway import create_internet_gateway
from vpc.route_table import create_route_table, create_route_to_internet, associate_route_table, create_route_to_nat_gateway
from vpc.nat_gateway import allocate_eip, create_nat_gateway
from vpc.security_group import (
    create_security_group,
    authorize_ingress,
    authorize_ingress_from_sg,
    generate_name
)

from auto_scaling_group import create_launch_template, create_auto_scaling_group
from load_balancer import create_target_group, create_load_balancer, create_listener
from ecs_cluster import create_ecs_cluster
from iam import create_task_role, create_execution_role, create_ecs_instance_role, create_ecs_instance_profile
from ecs_service import (
    register_task_definition,
    create_fargate_service,
    create_ec2_service,
    setup_service_autoscaling
)

from key_pair import create_key_pair

def main():
    EC2 = True
    FARGATE = True

    project_name = "ecs"
    my_cidr = "112.171.56.11/32"  # 본인의 IP 주소로 변경하세요.

    # VPC 생성
    vpc_id = create_vpc(project_name, "10.0.0.0/16")

    # EC2 런치 타입일 경우 Key Pair 생성
    if EC2:
        key_name = create_key_pair(project_name, "ecs-keypair")

    # 서브넷 생성
    public_subnet_1 = create_subnet(project_name, vpc_id, "10.0.1.0/24", "ap-northeast-2a", True, 1)
    public_subnet_2 = create_subnet(project_name, vpc_id, "10.0.2.0/24", "ap-northeast-2c", True, 2)
    private_subnet_1 = create_subnet(project_name, vpc_id, "10.0.3.0/24", "ap-northeast-2a", False, 3)
    private_subnet_2 = create_subnet(project_name, vpc_id, "10.0.4.0/24", "ap-northeast-2c", False, 4)

    # 인터넷 게이트웨이 생성
    igw_id = create_internet_gateway(project_name, vpc_id)

    # Elastic IP 할당 및 NAT 게이트웨이 생성
    allocation_id = allocate_eip(project_name)
    nat_gateway_id = create_nat_gateway(project_name, public_subnet_1, allocation_id)

    # 라우트 테이블 생성 및 설정
    public_route_table = create_route_table(project_name, vpc_id, 1)
    create_route_to_internet(public_route_table, igw_id)
    associate_route_table(public_route_table, public_subnet_1)
    associate_route_table(public_route_table, public_subnet_2)

    private_route_table_1 = create_route_table(project_name, vpc_id, 3)
    create_route_to_nat_gateway(private_route_table_1, nat_gateway_id)
    associate_route_table(private_route_table_1, private_subnet_1)

    private_route_table_2 = create_route_table(project_name, vpc_id, 4)
    create_route_to_nat_gateway(private_route_table_2, nat_gateway_id)
    associate_route_table(private_route_table_2, private_subnet_2)

    # ALB 보안 그룹 생성 및 인바운드 규칙 추가
    alb_sg_name = generate_name(project_name, "alb-sg")
    alb_sg_id = create_security_group(project_name, vpc_id, alb_sg_name, "ALB SG")
    authorize_ingress(alb_sg_id, 80, 'tcp', my_cidr)  # HTTP

    # Fargate 및 EC2에 맞는 보안 그룹 생성
    if FARGATE:
        fargate_task_sg_name = generate_name(project_name, "fargate-task-sg")
        fargate_task_sg_id = create_security_group(project_name, vpc_id, fargate_task_sg_name, "FARGATE TASK SG")
        authorize_ingress_from_sg(fargate_task_sg_id, 80, 'tcp', alb_sg_id)

    if EC2:
        ec2_task_sg_name = generate_name(project_name, "ec2-task-sg")
        ec2_task_sg_id = create_security_group(project_name, vpc_id, ec2_task_sg_name, "EC2 TASK SG")
        authorize_ingress_from_sg(ec2_task_sg_id, 80, 'tcp', alb_sg_id)

    # 타겟 그룹 생성
    target_group_arns = []
    if FARGATE:
        target_group_arn_fargate = create_target_group(project_name, vpc_id, "fargate", launch_type='FARGATE')
        target_group_arns.append(target_group_arn_fargate)

    if EC2:
        target_group_arn_ec2 = create_target_group(project_name, vpc_id, "ec2", launch_type='EC2')
        target_group_arns.append(target_group_arn_ec2)

    # 로드 밸런서 생성
    alb_arn = create_load_balancer(project_name, [public_subnet_1, public_subnet_2], [alb_sg_id])

    # 리스너 생성
    listener_arn = create_listener(project_name, alb_arn, target_group_arns)

    # ECS 클러스터 생성
    cluster_arn = create_ecs_cluster(project_name)
    cluster_name = cluster_arn.split('/')[-1]

    # IAM 역할 생성
    task_role_arn = create_task_role(project_name)
    execution_role_arn = create_execution_role(project_name)

    # ECS 태스크 정의 등록
    if FARGATE:
        task_definition_arn_fargate = register_task_definition(
            project_name=project_name,
            task_role_arn=task_role_arn,
            execution_role_arn=execution_role_arn,
            container_name="fargate-nginx",
            image="357836924303.dkr.ecr.ap-northeast-2.amazonaws.com/nginx:fargate",
            cpu=256,
            memory=512,
            port_mappings=[{'containerPort': 80, 'protocol': 'tcp'}],
            environment_vars=[],
            launch_type='FARGATE'
        )

    if EC2:
        task_definition_arn_ec2 = register_task_definition(
            project_name=project_name,
            task_role_arn=task_role_arn,
            execution_role_arn=execution_role_arn,
            container_name="ec2-nginx",
            image="357836924303.dkr.ecr.ap-northeast-2.amazonaws.com/nginx:ec2",
            cpu=256,
            memory=512,
            port_mappings=[{'containerPort': 80, 'hostPort': 80, 'protocol': 'tcp'}],
            environment_vars=[],
            launch_type='EC2'
        )

    # ECS 서비스 생성
    if FARGATE:
        service_arn_fargate = create_fargate_service(
            cluster_arn=cluster_arn,
            project_name=project_name,
            task_definition_arn=task_definition_arn_fargate,
            desired_count=1,
            subnet_ids=[private_subnet_1, private_subnet_2],
            security_group_id=fargate_task_sg_id,
            target_group_arns=[target_group_arn_fargate],
            load_balancer_arn=alb_arn
        )

    if EC2:
        # User Data 설정
        ecs_instance_role_name = create_ecs_instance_role(project_name)

        # IAM 인스턴스 프로파일 생성 및 역할 연결 후 대기
        ecs_instance_profile_name = create_ecs_instance_profile(project_name, ecs_instance_role_name)
        time.sleep(3)

        user_data_script = f"""#!/bin/bash
echo "ECS_CLUSTER={cluster_name}" >> /etc/ecs/ecs.config
"""
        user_data_encoded = base64.b64encode(user_data_script.encode('utf-8')).decode('utf-8')

        # Launch Template 생성
        launch_template_name = generate_name(project_name, "launch-template")
        create_launch_template(
            template_name=launch_template_name,
            ami_id='ami-0094452d83bc4b140',  # 최신 ECS Optimized AMI ID로 교체
            instance_type='t2.micro',
            security_group_ids=[ec2_task_sg_id],
            key_name=key_name,
            iam_instance_profile_name=ecs_instance_profile_name,
            user_data=user_data_encoded
        )

    # ECS 서비스 오토스케일링 설정
    if FARGATE:
        setup_service_autoscaling(
            cluster_arn=cluster_arn,
            service_arn=service_arn_fargate,
            min_capacity=1,
            max_capacity=5,
            target_cpu_utilization=70
        )

    print("모든 리소스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()
