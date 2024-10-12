[수동마운트]
새 볼륨을 ext4 파일 시스템으로 포맷
sudo mkfs -t ext4 /dev/xvdf
---
마운트할 디렉토리를 생성하고, EBS 볼륨을 마운트합니다:
sudo mkdir /mnt/ebs
sudo mount /dev/xvdf /mnt/ebs
---
마운트된 디스크를 확인합니다:
df -h
---
테스트 파일을 생성하여 데이터가 저장되는지 확인합니다:
sudo touch /mnt/ebs/testfile.txt


[자동마운트]
---
EBS 볼륨을 자동으로 마운트하도록 설정하기 위해 /etc/fstab 파일에 등록합니다:
sudo blkid

---
/etc/fstab 파일을 열어 UUID를 추가합니다:
sudo vi /etc/fstab
다음 형식으로 추가:
UUID=<볼륨의 UUID> /mnt/ebs ext4 defaults,nofail 0 2
sudo mount -a
---
