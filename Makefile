.PHONY: ansible terraform

fmt:
	@terraform fmt terraform

tf-up: fmt
	@cd terraform && \
		terraform apply -auto-approve

ansible-up:
	@cd ansible && \
		ANSIBLE_TIMEOUT=120 ansible-playbook cluster.yml -i inventory/hosts.ini --forks 25

sleep:
	@echo "wait for 30 seconds so the VMs are all ready"
	@sleep 30

up:	tf-up sleep ansible-up

down:
	@cd terraform && \
		terraform destroy -auto-approve
