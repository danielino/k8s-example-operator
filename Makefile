.PHONY: all
K := kubectl
KAPP := $(K) apply -f
DKBUILD := docker build -t 

all: docker-build deploy_operator deploy_instance

docker-build:
	eval $(minikube docker-env)
	$(DKBUILD) exampleapp:latest app
	$(DKBUILD) exampleoperator:latest operator

deploy_operator:
	$(KAPP) k8s/namespace.yml
	$(KAPP) k8s/crd.yml
	$(KAPP) k8s/serviceaccount.yml
	$(KAPP) k8s/rbac.yml
	$(KAPP) k8s/operator.yml
	
deploy_instance:
	$(KAPP) k8s/example.yml