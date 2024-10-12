# ecs_service.py
import boto3
import json

ecs = boto3.client('ecs')
application_autoscaling = boto3.client('application-autoscaling')

def generate_name(project_name, resource_type):
    return f"{project_name}-{resource_type}"

def register_task_definition(project_name, task_role_arn, execution_role_arn, container_name, image, cpu, memory, port_mappings=[], environment_vars=[], launch_type='FARGATE'):
    task_family = generate_name(project_name, "task")
    
    container_definitions = [
        {
            "name": container_name,
            "image": image,
            "essential": True,
            "cpu": cpu,
            "memory": memory,
            "portMappings": port_mappings,
            "environment": environment_vars,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/aws/nginx",
                    "awslogs-create-group": "true",
                    "awslogs-region": "ap-northeast-2",
                    "awslogs-stream-prefix": "nginx"
                }
            }
        }
    ]
    
    requires_compatibilities = ['FARGATE'] if launch_type == 'FARGATE' else ['EC2']
    network_mode = 'awsvpc' if launch_type == 'FARGATE' else 'bridge'
    
    response = ecs.register_task_definition(
        family=task_family,
        networkMode=network_mode,
        executionRoleArn=execution_role_arn,
        taskRoleArn=task_role_arn,
        containerDefinitions=container_definitions,
        requiresCompatibilities=requires_compatibilities,
        cpu=str(cpu),
        memory=str(memory)
    )
    
    task_definition_arn = response['taskDefinition']['taskDefinitionArn']
    print(f"태스크 정의 등록됨: {task_definition_arn}")
    return task_definition_arn

def create_fargate_service(cluster_arn, project_name, task_definition_arn, desired_count, subnet_ids, security_group_id, target_group_arns, load_balancer_arn):
    service_name = generate_name(project_name, "service")
    
    response = ecs.create_service(
        cluster=cluster_arn,
        serviceName=service_name,
        taskDefinition=task_definition_arn,
        desiredCount=desired_count,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': [security_group_id],
                'assignPublicIp': 'DISABLED'
            }
        },
        loadBalancers=[
            {
                'targetGroupArn': target_group_arns[0],  # 첫 번째 타겟 그룹 사용
                'containerName': 'fargate-nginx',
                'containerPort': 80
            }
        ],
        tags=[
            {
                'key': 'Name',
                'value': service_name
            }
        ],
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )
    
    service_arn = response['service']['serviceArn']
    print(f"ECS Fargate 서비스 생성됨: {service_name} (ARN: {service_arn})")
    return service_arn

def create_ec2_service(cluster_arn, project_name, task_definition_arn, desired_count, subnet_ids, security_group_id, target_group_arns, load_balancer_arn):
    service_name = generate_name(project_name, "service")
    
    response = ecs.create_service(
        cluster=cluster_arn,
        serviceName=service_name,
        taskDefinition=task_definition_arn,
        desiredCount=desired_count,
        launchType='EC2',
        loadBalancers=[
            {
                'targetGroupArn': target_group_arns[0],  # 첫 번째 타겟 그룹 사용
                'containerName': 'ec2-nginx',
                'containerPort': 80
            }
        ],
        tags=[
            {
                'key': 'Name',
                'value': service_name
            }
        ],
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )
    
    service_arn = response['service']['serviceArn']
    print(f"ECS EC2 서비스 생성됨: {service_name} (ARN: {service_arn})")
    return service_arn

def setup_service_autoscaling(cluster_arn, service_arn, min_capacity, max_capacity, target_cpu_utilization):
    resource_id = f'service/{cluster_arn.split("/")[-1]}/{service_arn.split("/")[-1]}'
    
    application_autoscaling.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId=resource_id,
        ScalableDimension='ecs:service:DesiredCount',
        MinCapacity=min_capacity,
        MaxCapacity=max_capacity
    )
    print(f"스케일링 대상 등록됨: {resource_id} (Min: {min_capacity}, Max: {max_capacity})")
    
    policy_name = f"{generate_name('scale', 'policy')}-cpu"
    response = application_autoscaling.put_scaling_policy(
        PolicyName=policy_name,
        ServiceNamespace='ecs',
        ResourceId=resource_id,
        ScalableDimension='ecs:service:DesiredCount',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': target_cpu_utilization,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
            },
            'ScaleOutCooldown': 60,
            'ScaleInCooldown': 60
        }
    )
    print(f"스케일링 정책 생성됨: {policy_name}")
    return response['PolicyARN']
