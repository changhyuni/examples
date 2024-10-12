import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type):
    """
    프로젝트 이름과 리소스 타입을 사용하여 고유한 이름을 생성합니다.
    """
    return f"{project_name}-{resource_type}"

def create_security_group(project_name, vpc_id, description):
    """
    지정된 VPC에 보안 그룹을 생성하고 이름 태그를 할당합니다.
    """
    sg_name = generate_name(project_name, "sg")
    response = ec2.create_security_group(
        GroupName=sg_name,
        Description=description,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {'Key': 'Name', 'Value': sg_name}
                ]
            }
        ]
    )
    sg_id = response['GroupId']
    print(f"보안 그룹 생성됨: {sg_name} (ID: {sg_id})")
    return sg_id

def authorize_ingress(sg_id, port, protocol, cidr):
    """
    보안 그룹에 인바운드 규칙을 추가합니다.
    """
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': protocol,
                'FromPort': port,
                'ToPort': port,
                'IpRanges': [{'CidrIp': cidr}]
            }
        ]
    )
    print(f"보안 그룹 {sg_id}에 인바운드 규칙 추가됨: {protocol} 포트 {port} from {cidr}")
