"""A Python Pulumi program"""

import pulumi
from pulumi_openstack import compute, networking


config = pulumi.Config()
network_name = config.require("network_name")

with open(config.require("public_key_path"), "r") as pk:
    cluster_keypair = compute.Keypair("cluster", name="cluster", public_key=pk.read())

secgroup = networking.SecGroup(
    "cluster",
    name="cluster",
    description="Cluster-wide communication for internal nodes",
    delete_default_rules=True,
)

secgroup_rule = networking.SecGroupRule(
    "cluster",
    direction="ingress",
    ethertype="IPv4",
    remote_group_id=secgroup.id,
    security_group_id=secgroup.id,
)

network = networking.Network(network_name)

# bastion

bastion_secgroup = networking.SecGroup(
    "bastion",
    name="bastion",
    description="Bastion node",
    delete_default_rules=True,
)

bastion_secgroup_ingress = networking.SecGroupRule(
    "bastion_secgroup_ingress",
    direction="ingress",
    ethertype="IPv4",
    protocol="tcp",
    port_range_min=22,
    port_range_max=22,
    remote_ip_prefix="0.0.0.0/0",
    security_group_id=bastion_secgroup.id,
)

bastion_secgroup_egress = networking.SecGroupRule(
    "bastion_secgroup_egress",
    direction="egress",
    ethertype="IPv4",
    remote_ip_prefix="0.0.0.0/0",
    security_group_id=bastion_secgroup.id,
)

bastion = compute.Instance(
    "bastion",
    name="bastion",
    image_name=config.require("image_name"),
    flavor_name=config.require("flavor_bastion"),
    key_pair=cluster_keypair.name,
    security_groups=[secgroup, bastion_secgroup],
    networks=[compute.InstanceNetworkArgs(name=network_name)],
)

bastion_fip = compute.FloatingIpAssociate(
    "bastion",
    floating_ip=config.require("floating_ip_bastion"),
    instance_id=bastion.id,
)
