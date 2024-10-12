import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def create_internet_gateway(project_name, vpc_id):
    """
    인터넷 게이트웨이를 생성하고 VPC에 연결하며 이름 태그를 할당합니다.
    """
    igw_name = generate_name(project_name, "igw")
    response = ec2.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {'Key': 'Name', 'Value': igw_name}
                ]
            }
        ]
    )
    igw_id = response['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"인터넷 게이트웨이 생성 및 연결됨: {igw_name} (ID: {igw_id})")
    return igw_id
