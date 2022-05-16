.PHONY: terraform

fmt:
	@terraform fmt terraform

up: fmt
	@cd terraform && \
		terraform apply -auto-approve

down:
	@cd terraform && \
		terraform destroy -auto-approve
