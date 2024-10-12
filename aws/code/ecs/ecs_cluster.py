# ecs.py
import boto3

ecs = boto3.client('ecs')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def create_ecs_cluster(project_name):
    """
    ECS 클러스터를 생성하고 이름 태그를 할당합니다.
    """
    cluster_name = generate_name(project_name, "cluster")
    response = ecs.create_cluster(
        clusterName=cluster_name,
        tags=[
            {
                'key': 'Name',
                'value': cluster_name
            }
        ]
    )
    cluster_arn = response['cluster']['clusterArn']
    print(f"ECS 클러스터 생성됨: {cluster_name} (ARN: {cluster_arn})")
    return cluster_arn
