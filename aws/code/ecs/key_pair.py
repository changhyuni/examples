import boto3
import os

def create_key_pair(project_name, key_name):
    """
    EC2 인스턴스에 사용할 Key Pair를 생성하고, 로컬에 저장하는 함수
    """
    ec2 = boto3.client('ec2')
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        private_key = key_pair['KeyMaterial']
        
        key_file_path = f"./{key_name}.pem"
        with open(key_file_path, 'w') as key_file:
            key_file.write(private_key)
        
        print(f"Key Pair '{key_name}'가 생성되었고, {key_file_path}에 저장되었습니다.")
        return key_name
    except ec2.exceptions.ClientError as e:
        if 'InvalidKeyPair.Duplicate' in str(e):
            print(f"이미 존재하는 Key Pair '{key_name}'를 사용합니다.")
            return key_name
        else:
            raise e
