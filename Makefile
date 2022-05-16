.PHONY: terraform

fmt:
	@terraform fmt terraform

up: fmt
	@cd terraform && \
		terraform apply -var-file=data.tfvars -auto-approve

down:
	@cd terraform && \
		terraform destroy -var-file=data.tfvars -auto-approve
