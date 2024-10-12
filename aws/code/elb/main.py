from vpc import create_vpc
from subnet import create_subnet
from internet_gateway import create_internet_gateway
from route_table import create_route_table, create_route_to_internet, associate_route_table
from security_group import create_security_group, authorize_ingress, authorize_ingress_from_sg, generate_name
from auto_scaling_group import create_launch_template, create_auto_scaling_group
from key_pair import create_key_pair
from load_balancer import create_target_group, create_load_balancer, create_listener

def main():
    project_name = "ec2"
    my_cidr = "112.171.56.11/32"  # 본인의 IP 주소로 변경하세요.

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

    # 인스턴스 보안 그룹 생성 및 인바운드 규칙 추가
    instance_sg_name = generate_name(project_name, "instance-sg")
    sg_id = create_security_group(project_name, vpc_id, instance_sg_name, "Instance SG")
    authorize_ingress(sg_id, 22, 'tcp', my_cidr)  # SSH

    # ALB 보안 그룹 생성 및 인바운드 규칙 추가
    alb_sg_name = generate_name(project_name, "alb-sg")
    alb_sg_id = create_security_group(project_name, vpc_id, alb_sg_name, "ALB SG")
    authorize_ingress(alb_sg_id, 80, 'tcp', my_cidr)  # HTTP

    # ALB가 인스턴스에 접근할 수 있도록 인스턴스 SG에 인바운드 규칙 추가
    authorize_ingress_from_sg(sg_id, 80, 'tcp', alb_sg_id)

    # AMI 및 인스턴스 유형 설정
    ami_id = "ami-0e18fe6ecdad223e5"
    instance_type = "t2.micro"

    # 타겟 그룹 생성
    target_group_arn_a = create_target_group(project_name, vpc_id, "a")
    target_group_arn_b = create_target_group(project_name, vpc_id, "b")

    # 로드 밸런서 생성
    alb_arn = create_load_balancer(project_name, [public_subnet_1, public_subnet_2], [alb_sg_id])

    # 리스너 생성
    listener_arn = create_listener(project_name, alb_arn, [target_group_arn_a, target_group_arn_b])

    # 런치 템플릿 생성 (a와 b)
    user_data_script_a = '''#!/bin/bash
    yum update -y
    yum install nginx -y
    echo "a" > /usr/share/nginx/html/index.html
    systemctl start nginx
    systemctl enable nginx
    '''

    user_data_script_b = '''#!/bin/bash
    yum update -y
    yum install nginx -y
    echo "b" > /usr/share/nginx/html/index.html
    systemctl start nginx
    systemctl enable nginx
    '''

    launch_template_name_a = create_launch_template(project_name + "-a", ami_id, instance_type, key_name, sg_id, user_data_script_a)
    launch_template_name_b = create_launch_template(project_name + "-b", ami_id, instance_type, key_name, sg_id, user_data_script_b)

    # 오토 스케일링 그룹 생성 (a와 b)
    auto_scaling_group_name_a = create_auto_scaling_group(project_name + "-a", "asg-a", launch_template_name_a, 1, 3, [public_subnet_1, public_subnet_2], [target_group_arn_a])
    auto_scaling_group_name_b = create_auto_scaling_group(project_name + "-b", "asg-b", launch_template_name_b, 1, 3, [public_subnet_1, public_subnet_2], [target_group_arn_b])

    print("모든 리소스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()
