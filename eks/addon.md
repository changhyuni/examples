[keda]
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace --version 2.16.1
helm uninstall keda -n keda

[karpenter]
helm repo add karpenter https://charts.karpenter.sh/
helm install karpenter oci://public.ecr.aws/karpenter/karpenter --version 1.1.1 --namespace utils --create-namespace \
  --set "settings.clusterName=dev-cacoabank-cluster" 