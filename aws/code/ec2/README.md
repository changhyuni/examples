[ssh]
ssh -i ./ec2.pem {IP}

[ip]
curl https://checkip.amazonaws.com  

[stress]
stress --cpu 2 --timeout 600

[cloud-init]
cat /var/log/cloud-init-output.log

[imds]
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/"
curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/instance-id"
curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/ami-id"
curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam/security-credentials/list_users" 

aws iam list-users