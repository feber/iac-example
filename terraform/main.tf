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

### cluster wide keypair ###

resource "openstack_compute_keypair_v2" "cluster" {
  name       = "cluster"
  public_key = chomp(file(var.public_key_path))
}

### bastion ###

resource "openstack_compute_floatingip_associate_v2" "bastion" {
  floating_ip = var.floating_ip_bastion
  instance_id = openstack_compute_instance_v2.bastion[0].id
}

resource "openstack_networking_secgroup_v2" "bastion" {
  name                 = "bastion"
  count                = var.number_of_bastions == 1 ? 1 : 0
  description          = "Bastion node"
  delete_default_rules = true
}

resource "openstack_networking_secgroup_rule_v2" "bastion" {
  count             = var.number_of_bastions
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = "22"
  port_range_max    = "22"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.bastion[0].id
}

resource "openstack_networking_secgroup_rule_v2" "bastion_egress" {
  count             = length(var.bastion_allowed_egress_ips)
  direction         = "egress"
  ethertype         = "IPv4"
  remote_ip_prefix  = var.bastion_allowed_egress_ips[count.index]
  security_group_id = openstack_networking_secgroup_v2.bastion[0].id
}

resource "openstack_compute_instance_v2" "bastion" {
  name        = "bastion-${count.index + 1}"
  count       = var.number_of_bastions
  image_name  = var.image_name
  flavor_name = var.flavor_bastion
  key_pair    = openstack_compute_keypair_v2.cluster.name

  network {
    name = var.network_name
  }

  security_groups = [openstack_networking_secgroup_v2.bastion[0].name]
}

### workers ###

resource "openstack_networking_secgroup_v2" "worker" {
  name                 = "worker"
  count                = var.number_of_workers != "" ? 1 : 0
  description          = "Worker nodes"
  delete_default_rules = true
}

resource "openstack_networking_secgroup_rule_v2" "worker_egress" {
  count             = length(var.worker_allowed_egress_ips)
  direction         = "egress"
  ethertype         = "IPv4"
  remote_ip_prefix  = var.worker_allowed_egress_ips[count.index]
  security_group_id = openstack_networking_secgroup_v2.worker[0].id
}

resource "openstack_compute_instance_v2" "worker" {
  name        = "worker-${count.index + 1}"
  count       = var.number_of_workers
  image_name  = var.image_name
  flavor_name = var.flavor_worker
  key_pair    = openstack_compute_keypair_v2.cluster.name

  network {
    name = var.network_name
  }

  security_groups = [openstack_networking_secgroup_v2.worker[0].name]
}
