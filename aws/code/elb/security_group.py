import boto3

ec2 = boto3.client('ec2')

def generate_name(project_name, resource_type):
    return f"{project_name}-{resource_type}"

def create_security_group(project_name, vpc_id, sg_name, description):
    try:
        response = ec2.create_security_group(
            GroupName=sg_name,
            Description=description,
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [{'Key': 'Name', 'Value': sg_name}]
                }
            ]
        )
        sg_id = response['GroupId']
        print(f"보안 그룹 생성됨: {sg_name} (ID: {sg_id})")
    except ec2.exceptions.ClientError as e:
        if 'InvalidGroup.Duplicate' in str(e):
            # 이미 존재하는 보안 그룹을 가져옵니다.
            response = ec2.describe_security_groups(
                Filters=[
                    {'Name': 'group-name', 'Values': [sg_name]},
                    {'Name': 'vpc-id', 'Values': [vpc_id]}
                ]
            )
            sg_id = response['SecurityGroups'][0]['GroupId']
            print(f"이미 존재하는 보안 그룹 사용: {sg_name} (ID: {sg_id})")
        else:
            raise e
    return sg_id

def authorize_ingress(sg_id, port, protocol, cidr):
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': protocol,
            'FromPort': port,
            'ToPort': port,
            'IpRanges': [{'CidrIp': cidr}]
        }]
    )
    print(f"보안 그룹 {sg_id}에 인바운드 규칙 추가됨: {protocol} 포트 {port} from {cidr}")

def authorize_ingress_from_sg(sg_id, port, protocol, source_sg_id):
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': protocol,
            'FromPort': port,
            'ToPort': port,
            'UserIdGroupPairs': [{'GroupId': source_sg_id}]
        }]
    )
    print(f"보안 그룹 {sg_id}에 인바운드 규칙 추가됨: {protocol} 포트 {port} from 보안 그룹 {source_sg_id}")
