[prometheus]
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml --version 67.5.0
helm upgrade prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml
helm uninstall prometheus -n monitoring
kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" -n monitoring | base64 --decode ; echo

[mimir]
helm repo add grafana https://grafana.github.io/helm-charts
helm install mimir grafana/mimir-distributed -n monitoring -f values.yaml --version 5.5.1
helm upgrade mimir grafana/mimir-distributed -n monitoring -f values.yaml
helm uninstall mimir -n monitoring
mimir endpoint: http://mimir-nginx.monitoring.svc:80/prometheus

[loki]
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-distributed -n monitoring --version 0.80.0 -f values.yaml
helm upgrade loki grafana/loki-distributed -n monitoring -f values.yaml
helm uninstall loki -n monitoring
loki endpoint : http://loki-loki-distributed-gateway.monitoring.svc.cluster.local:80

[vector]
helm repo add vector https://helm.vector.dev
helm install vector vector/vector -n monitoring --version 0.38.1 -f values.yaml
helm upgrade vector vector/vector -n monitoring -f values.yaml
helm uninstall vector -n monitoring

[tempo]
helm repo add grafana https://grafana.github.io/helm-charts
helm install tempo grafana/tempo-distributed -n monitoring --version 1.27.0 -f values.yaml
helm upgrade tempo grafana/tempo-distributed -n monitoring -f values.yaml
helm uninstall tempo -n monitoring

[opentele-metry]
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install opentelemetry open-telemetry/opentelemetry-collector -n monitoring --version 0.111.0 -f values.yaml
helm upgrade opentelemetry open-telemetry/opentelemetry-collector -n monitoring
helm uninstall opentelemetry -n monitoring