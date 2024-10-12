import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type, index):
    """
    프로젝트 이름, 리소스 타입 및 인덱스를 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}-{index}"

def create_route_table(project_name, vpc_id, index):
    """
    지정된 VPC에 라우트 테이블을 생성하고 이름 태그를 할당합니다.
    """
    route_table_name = generate_name(project_name, "rtb", index)
    response = ec2.create_route_table(
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {'Key': 'Name', 'Value': route_table_name}
                ]
            }
        ]
    )
    route_table_id = response['RouteTable']['RouteTableId']
    print(f"라우트 테이블 생성됨: {route_table_name} (ID: {route_table_id})")
    return route_table_id

def create_route_to_internet(route_table_id, igw_id):
    """
    라우트 테이블에 인터넷 게이트웨이로의 기본 라우트를 생성합니다.
    """
    ec2.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )
    print(f"인터넷 게이트웨이 {igw_id}로의 라우트가 라우트 테이블 {route_table_id}에 추가되었습니다.")

def create_route_to_nat_gateway(route_table_id, nat_gateway_id):
    """
    라우트 테이블에 NAT 게이트웨이로의 기본 라우트를 생성합니다.
    """
    ec2.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=nat_gateway_id
    )
    print(f"NAT 게이트웨이 {nat_gateway_id}로의 라우트가 라우트 테이블 {route_table_id}에 추가되었습니다.")

def associate_route_table(route_table_id, subnet_id):
    """
    라우트 테이블을 지정된 서브넷에 연결합니다.
    """
    ec2.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)
    print(f"라우트 테이블 {route_table_id}이(가) 서브넷 {subnet_id}에 연결되었습니다.")
