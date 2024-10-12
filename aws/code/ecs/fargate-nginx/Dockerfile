# 베이스 이미지로 nginx의 경량화된 Alpine 버전 사용
FROM nginx:latest

# 현재 디렉토리의 index.html 파일을 컨테이너의 nginx 기본 웹 페이지 디렉토리에 복사
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

# 컨테이너가 실행될 때 nginx를 포그라운드에서 실행하도록 설정
CMD ["nginx", "-g", "daemon off;"]
