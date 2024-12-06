#!/bin/bash
set -ex

# kubelet 오버라이드 JSON 적용
# kubelet_overrides_json 변수가 "{}"가 아니라면, 해당 내용을 기존 kubelet-config.json에 merge
if [ "${kubelet_overrides_json}" != "{}" ]; then
    yum install -y jq
    echo '${kubelet_overrides_json}' > /tmp/kubelet-overrides.json
    jq -s '.[0] * .[1]' /etc/kubernetes/kubelet/kubelet-config.json /tmp/kubelet-overrides.json > /etc/kubernetes/kubelet/kubelet-config-merged.json
    mv /etc/kubernetes/kubelet/kubelet-config-merged.json /etc/kubernetes/kubelet/kubelet-config.json
fi

yum update -y && yum install vim wget curl -y

# bootstrap 실행 (kubelet 설정 반영은 /etc/eks/bootstrap.sh 실행 시 자동 반영)
# kubelet-extra-args는 필요시 추가 가능. 예: --kubelet-extra-args '--node-labels=...'
/etc/eks/bootstrap.sh '${cluster_name}' \
  --apiserver-endpoint '${endpoint}' \
  --b64-cluster-ca '${cluster_auth_base64}'
