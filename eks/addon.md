[keda]
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace
helm uninstall keda -n keda

[karpenter]
helm repo add karpenter https://charts.karpenter.sh/
helm install karpenter oci://public.ecr.aws/karpenter/karpenter --version 1.1.1 --namespace utils --create-namespace \
  --set "settings.clusterName=dev-cacoabank-cluster" 

[external-secret]
helm repo add external-secrets https://charts.external-secrets.io
helm repo update
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace --set installCRDs=true --set webhook.port=9443

[external-dns]
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update external-dns
helm install external-dns external-dns/external-dns --namespace external-secrets --create-namespace --version 1.15.0