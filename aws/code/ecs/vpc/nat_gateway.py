import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def allocate_eip(project_name):
    """
    NAT 게이트웨이에 사용할 Elastic IP를 할당하고 이름 태그를 지정합니다.
    """
    eip_name = generate_name(project_name, "eip")
    response = ec2.allocate_address(
        Domain='vpc',
        TagSpecifications=[
            {
                'ResourceType': 'elastic-ip',
                'Tags': [
                    {'Key': 'Name', 'Value': eip_name}
                ]
            }
        ]
    )
    allocation_id = response['AllocationId']
    print(f"Elastic IP 할당됨: {eip_name} (할당 ID: {allocation_id})")
    return allocation_id

def create_nat_gateway(project_name, subnet_id, allocation_id):
    """
    지정된 서브넷에 NAT 게이트웨이를 생성하고 Elastic IP를 연결하며 이름 태그를 할당합니다.
    """
    nat_gateway_name = generate_name(project_name, "nat-gateway")
    response = ec2.create_nat_gateway(
        SubnetId=subnet_id,
        AllocationId=allocation_id,
        TagSpecifications=[
            {
                'ResourceType': 'natgateway',
                'Tags': [
                    {'Key': 'Name', 'Value': nat_gateway_name}
                ]
            }
        ]
    )
    nat_gateway_id = response['NatGateway']['NatGatewayId']
    print(f"NAT 게이트웨이 생성됨: {nat_gateway_name} (ID: {nat_gateway_id})")

    # NAT 게이트웨이가 사용 가능해질 때까지 대기
    print("NAT 게이트웨이가 활성화될 때까지 대기 중입니다...")
    waiter = ec2.get_waiter('nat_gateway_available')
    waiter.wait(NatGatewayIds=[nat_gateway_id])
    print(f"NAT 게이트웨이 활성화됨: {nat_gateway_id}")

    return nat_gateway_id
