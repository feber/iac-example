variable "public_key_path" {}

variable "private_key_path" {}

variable "image_name" {}

variable "ssh_user" {}

variable "number_of_bastions" {}

variable "flavor_bastion" {}

variable "floating_ip_bastion" {}

variable "number_of_workers" {}

variable "flavor_worker" {}

variable "network_name" {}

variable "bastion_allowed_egress_ips" {
  description = "An array of CIDRs allowed for egress traffic"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "worker_allowed_egress_ips" {
  description = "An array of CIDRs allowed for egress traffic"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
