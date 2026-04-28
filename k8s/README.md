# Kubernetes deployment notes

This directory contains working manifest sets for the assignment.

## Base

- `base/namespace.yaml`
- `base/configmap.yaml`
- `base/service.yaml`

## Strategies

- `strategies/rolling`: standard rolling update deployment
- `strategies/blue-green`: blue and green deployments plus active/preview services
- `strategies/canary`: stable + canary split using replica weighting
- `strategies/ab-testing`: header-based routing with NGINX ingress
- `strategies/shadow`: mirrored traffic with NGINX ingress

## Quick start with Minikube

```powershell
minikube start --driver=docker
minikube addons enable ingress
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-k8s.ps1 -Strategy rolling -Image docker.io/<dockerhub-user>/aceest-fitness-gym:v1.0.0
minikube service aceest-service -n aceest-devops --url
```

## Blue-green switch

Use the active service file that matches the color you want live:

```powershell
kubectl apply -f k8s/strategies/blue-green/service-active-green.yaml
```

Rollback:

```powershell
kubectl apply -f k8s/strategies/blue-green/service-active-blue.yaml
```

## A/B and shadow notes

These rely on the NGINX ingress addon in Minikube.

- A/B testing routes requests with header `x-ab-test: B` to variant B
- Shadow deployment mirrors traffic from `aceest-shadow.local` to the shadow service
