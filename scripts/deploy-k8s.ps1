param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("rolling", "blue-green", "canary", "ab-testing", "shadow")]
    [string]$Strategy,

    [string]$Namespace = "aceest-devops",
    [string]$Image = "aceest-fitness-gym:latest"
)

$ErrorActionPreference = "Stop"

function Invoke-KubectlApply {
    param([string]$Path)
    if (Test-Path $Path) {
        kubectl apply -f $Path
    }
}

Invoke-KubectlApply "k8s/base/namespace.yaml"
Invoke-KubectlApply "k8s/base/configmap.yaml"

switch ($Strategy) {
    "rolling" {
        Invoke-KubectlApply "k8s/base/service.yaml"
        Invoke-KubectlApply "k8s/strategies/rolling/deployment.yaml"
        kubectl -n $Namespace set image deployment/aceest-app aceest-app=$Image
        kubectl -n $Namespace rollout status deployment/aceest-app
    }
    "blue-green" {
        Invoke-KubectlApply "k8s/strategies/blue-green/deployment-blue.yaml"
        Invoke-KubectlApply "k8s/strategies/blue-green/deployment-green.yaml"
        Invoke-KubectlApply "k8s/strategies/blue-green/service-active-blue.yaml"
        Invoke-KubectlApply "k8s/strategies/blue-green/service-preview.yaml"
        kubectl -n $Namespace set image deployment/aceest-blue aceest-app=$Image
        kubectl -n $Namespace set image deployment/aceest-green aceest-app=$Image
        kubectl -n $Namespace rollout status deployment/aceest-blue
        kubectl -n $Namespace rollout status deployment/aceest-green
    }
    "canary" {
        Invoke-KubectlApply "k8s/strategies/canary/service.yaml"
        Invoke-KubectlApply "k8s/strategies/canary/deployment-stable.yaml"
        Invoke-KubectlApply "k8s/strategies/canary/deployment-canary.yaml"
        kubectl -n $Namespace set image deployment/aceest-stable aceest-app=$Image
        kubectl -n $Namespace set image deployment/aceest-canary aceest-app=$Image
        kubectl -n $Namespace rollout status deployment/aceest-stable
        kubectl -n $Namespace rollout status deployment/aceest-canary
    }
    "ab-testing" {
        Invoke-KubectlApply "k8s/strategies/ab-testing/deployment-a.yaml"
        Invoke-KubectlApply "k8s/strategies/ab-testing/deployment-b.yaml"
        Invoke-KubectlApply "k8s/strategies/ab-testing/service-a.yaml"
        Invoke-KubectlApply "k8s/strategies/ab-testing/service-b.yaml"
        Invoke-KubectlApply "k8s/strategies/ab-testing/ingress-a.yaml"
        Invoke-KubectlApply "k8s/strategies/ab-testing/ingress-b-canary.yaml"
        kubectl -n $Namespace set image deployment/aceest-variant-a aceest-app=$Image
        kubectl -n $Namespace set image deployment/aceest-variant-b aceest-app=$Image
        kubectl -n $Namespace rollout status deployment/aceest-variant-a
        kubectl -n $Namespace rollout status deployment/aceest-variant-b
    }
    "shadow" {
        Invoke-KubectlApply "k8s/strategies/shadow/deployment-primary.yaml"
        Invoke-KubectlApply "k8s/strategies/shadow/deployment-shadow.yaml"
        Invoke-KubectlApply "k8s/strategies/shadow/service-primary.yaml"
        Invoke-KubectlApply "k8s/strategies/shadow/ingress-shadow.yaml"
        kubectl -n $Namespace set image deployment/aceest-primary aceest-app=$Image
        kubectl -n $Namespace set image deployment/aceest-shadow aceest-app=$Image
        kubectl -n $Namespace rollout status deployment/aceest-primary
        kubectl -n $Namespace rollout status deployment/aceest-shadow
    }
}
