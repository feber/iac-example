terraform {
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "1.47.0"
    }
  }
}

# Configuration options, leave empty to use environment variables.
# Ref: https://registry.terraform.io/providers/terraform-provider-openstack/openstack/1.47.0
provider "openstack" {
}
