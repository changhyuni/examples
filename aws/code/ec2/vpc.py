import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def create_vpc(project_name, cidr_block):
    """
    지정된 CIDR 블록으로 VPC를 생성하고 이름 태그를 할당합니다.
    """
    vpc_name = generate_name(project_name, "vpc")
    response = ec2.create_vpc(
        CidrBlock=cidr_block,
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {'Key': 'Name', 'Value': vpc_name}
                ]
            }
        ]
    )
    vpc_id = response['Vpc']['VpcId']
    print(f"VPC 생성됨: {vpc_name} (ID: {vpc_id})")
    return vpc_id
