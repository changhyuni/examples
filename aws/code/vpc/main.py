import os
from vpc import create_vpc
from subnet import create_subnet
from internet_gateway import create_internet_gateway
from nat_gateway import allocate_eip, create_nat_gateway
from route_table import create_route_table, create_route_to_internet, create_route_to_nat_gateway, associate_route_table

def main():
    project_name = "june-project"

    # VPC 생성
    vpc_id = create_vpc(project_name, "10.0.0.0/16")

    # 서브넷 생성
    public_subnet_1 = create_subnet(project_name, vpc_id, "10.0.1.0/24", "ap-northeast-2a", True, 1)
    public_subnet_2 = create_subnet(project_name, vpc_id, "10.0.2.0/24", "ap-northeast-2b", True, 2)
    private_subnet_1 = create_subnet(project_name, vpc_id, "10.0.3.0/24", "ap-northeast-2a", False, 3)
    private_subnet_2 = create_subnet(project_name, vpc_id, "10.0.4.0/24", "ap-northeast-2b", False, 4)

    # 인터넷 게이트웨이 생성
    igw_id = create_internet_gateway(project_name, vpc_id)

    # Elastic IP 할당 및 NAT 게이트웨이 생성
    allocation_id = allocate_eip(project_name)
    nat_gateway_id = create_nat_gateway(project_name, public_subnet_1, allocation_id)

    # 라우트 테이블 생성 및 설정
    public_route_table = create_route_table(project_name, vpc_id, 1)
    create_route_to_internet(public_route_table, igw_id)
    associate_route_table(public_route_table, public_subnet_1)
    associate_route_table(public_route_table, public_subnet_2)

    private_route_table_1 = create_route_table(project_name, vpc_id, 2)
    create_route_to_nat_gateway(private_route_table_1, nat_gateway_id)
    associate_route_table(private_route_table_1, private_subnet_1)

    private_route_table_2 = create_route_table(project_name, vpc_id, 3)
    create_route_to_nat_gateway(private_route_table_2, nat_gateway_id)
    associate_route_table(private_route_table_2, private_subnet_2)

    print("모든 리소스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    main()
