from vpc import create_vpc
from subnet import create_subnet
from internet_gateway import create_internet_gateway
from route_table import create_route_table, create_route_to_internet, associate_route_table
from security_group import create_security_group, authorize_ingress
from auto_scaling_group import create_launch_template, create_auto_scaling_group, create_scaling_policy, create_cpu_alarm
from key_pair import create_key_pair 

def main():
    project_name = "ec2"

    # curl checkip.amazonaws.com 또 는
    # 네이버에 "내 아이피" 검색
    my_cidr = "112.171.56.11/32"

    # VPC 생성
    vpc_id = create_vpc(project_name, "10.0.0.0/16")

    # Key Pair 생성
    key_name = create_key_pair(project_name, "ec2")

    # 서브넷 생성
    public_subnet_1 = create_subnet(project_name, vpc_id, "10.0.1.0/24", "ap-northeast-2a", True, 1)
    public_subnet_2 = create_subnet(project_name, vpc_id, "10.0.2.0/24", "ap-northeast-2c", True, 2)

    # 인터넷 게이트웨이 생성
    igw_id = create_internet_gateway(project_name, vpc_id)

    # 라우트 테이블 생성 및 설정
    public_route_table = create_route_table(project_name, vpc_id, 1)
    create_route_to_internet(public_route_table, igw_id)
    associate_route_table(public_route_table, public_subnet_1)
    associate_route_table(public_route_table, public_subnet_2)

    # SG 생성 및 인바운드 규칙 추가 (HTTP, SSH)
    sg_id = create_security_group(project_name, vpc_id, "web")
    authorize_ingress(sg_id, 80, 'tcp', my_cidr)  # HTTP 80번 포트 (전체 허용)
    authorize_ingress(sg_id, 22, 'tcp', my_cidr)      # SSH 22번 포트 (현재 IP만 허용)

    # 퍼블릭 서브넷에 EC2 인스턴스 생성
    ami_id = "ami-0e18fe6ecdad223e5"
    instance_type = "t2.micro"

    # 런치 구성 및 오토 스케일링 그룹 생성
    user_data_script = '''#!/bin/bash
                          yum update -y
                          yum install nginx -y
                          systemctl start nginx
                          systemctl enable nginx
                       '''
    launch_template_name = create_launch_template(project_name, ami_id, instance_type, key_name, sg_id, user_data_script)

    # Auto Scaling Group 생성
    auto_scaling_group_name = create_auto_scaling_group(project_name, "auto-scaling-group", launch_template_name, 1, 3, [public_subnet_1, public_subnet_2])

    # Auto Scaling 정책 생성 및 적용
    scaling_policy_arn = create_scaling_policy(auto_scaling_group_name, project_name)
    
    # CPU 사용량 80% 이상일 때 트리거되는 CloudWatch 알람 생성 (스케일링 정책 ARN을 사용)
    create_cpu_alarm(auto_scaling_group_name, project_name, scaling_policy_arn)

    print("모든 리소스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()
