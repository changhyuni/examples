[kubeconfig]
aws eks update-kubeconfig --region ap-northeast-2 --name dev-cacoabank-cluster

[debug]
kubectl debug -it coredns-**  --image=busybox --target=coredns -n kube-system