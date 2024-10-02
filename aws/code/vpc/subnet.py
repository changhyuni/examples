import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type, index):
    """
    프로젝트 이름, 리소스 타입 및 인덱스를 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}-{index}"

def create_subnet(project_name, vpc_id, cidr_block, availability_zone, is_public, index):
    """
    지정된 VPC에 서브넷을 생성하고 이름 태그를 할당하며, 퍼블릭 IP 할당 설정을 적용합니다.
    """
    subnet_name = generate_name(project_name, "subnet", index)
    response = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=availability_zone,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {'Key': 'Name', 'Value': subnet_name}
                ]
            }
        ]
    )
    subnet_id = response['Subnet']['SubnetId']
    print(f"서브넷 생성됨: {subnet_name} (ID: {subnet_id}, AZ: {availability_zone})")

    # 퍼블릭 서브넷인 경우 퍼블릭 IP 자동 할당 활성화
    if is_public:
        ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={'Value': True})

    return subnet_id
