[ecr-login]
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 357836924303.dkr.ecr.ap-northeast-2.amazonaws.com"

[docker build]
docker buildx build --platform linux/amd64 --load -t 357836924303.dkr.ecr.ap-northeast-2.amazonaws.com/nginx:ec2 .
docker buildx build --platform linux/amd64 --load -t 357836924303.dkr.ecr.ap-northeast-2.amazonaws.com/nginx:fargate .