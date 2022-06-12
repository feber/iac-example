"""A Python Pulumi program"""

from unicodedata import name
from pulumi_openstack import compute, networking


with open("../testbed.pub", "r") as pk:
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

network = networking.Network("project_2004678")

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
    image_name="Ubuntu-20.04",
    flavor_name="standard.small",
    key_pair=cluster_keypair.name,
    security_groups=[secgroup, bastion_secgroup],
    networks=[compute.InstanceNetworkArgs(name="project_2004678")],
)

bastion_fip = compute.FloatingIpAssociate(
    "bastion",
    floating_ip="128.214.255.123",
    instance_id=bastion.id,
)
