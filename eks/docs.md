[kubeconfig]
aws eks update-kubeconfig --region ap-northeast-2 --name dev-cacoabank-cluster

[debug]
kubectl debug -it coredns-5b9dfbf96-565f8  --image=busybox --target=coredns -n kube-system

[aws-load-balacner-controller]
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller --set clusterName=dev-cacoabank-cluster -n kube-system --set serviceAccount.create=true --set replicaCount=1 --version 1.10.1

[storage]
AmazonEBSCSIDriverPolicy

[argocd]
helm repo add argo https://argoproj.github.io/argo-helm
helm -n argocd install argocd argo/argo-cd -f ./argocd.yaml --version 7.7.10
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
helm uninstall argocd -n argocd

[atlantis-token]
github token   : echo -n 'glpat-xx-example' > /tmp/github_token
github webhook : echo -n 'asdasdasdasd' > /tmp/github_secret
basic username : echo -n 'admin' > /tmp/username
basic password : echo -n 'asdasdasdasd' > /tmp/password

webhook secret: https://www.browserling.com/tools/random-string

kubectl create secret generic atlantis-vcs \
  --namespace atlantis \
  --from-file=/tmp/github_token \
  --from-file=/tmp/github_secret

kubectl create secret generic atlantis-basic-auth \
  --namespace atlantis \
  --from-file=/tmp/username \
  --from-file=/tmp/password

[atlantis]
helm repo add atlantis https://runatlantis.github.io/helm-charts
helm upgrade --install atlantis atlantis/atlantis -n atlantis -f values.yaml --version 5.12.0
helm uninstall atlantis -n atlantis


[atlantis-command]
https://www.runatlantis.io/docs/using-atlantis
