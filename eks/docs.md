[kubeconfig]
aws eks update-kubeconfig --region ap-northeast-2 --name dev-cacoabank-cluster

[debug]
kubectl debug -it coredns-5b9dfbf96-565f8  --image=busybox --target=coredns -n kube-system

[aws-load-balacner-controller]
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller --set clusterName=dev-cacoabank-cluster -n kube-system --set serviceAccount.create=true --set replicaCount=1

[storage]
AmazonEBSCSIDriverPolicy

[argocd]
helm repo add argo https://argoproj.github.io/argo-helm
helm -n argocd install argocd argo/argo-cd -f ./argocd.yaml
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

[atlantis]
helm repo add atlantis https://runatlantis.github.io/helm-charts
helm upgrade --install atlantis atlantis/atlantis -n atlantis -f values.yaml
webhook secret: https://www.browserling.com/tools/random-string
