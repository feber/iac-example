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


def bastion():
    """
    Responsible for security group, its rules, compute instance and
    floating IP association for bastion node(s).
    """

    # security group
    bastion_secgroup = networking.SecGroup(
        "bastion",
        name="bastion",
        description="Bastion node",
        delete_default_rules=True,
    )

    # security group rules
    networking.SecGroupRule(
        "bastion_secgroup_ingress",
        direction="ingress",
        ethertype="IPv4",
        protocol="tcp",
        port_range_min=22,
        port_range_max=22,
        remote_ip_prefix="0.0.0.0/0",
        security_group_id=bastion_secgroup.id,
    )

    networking.SecGroupRule(
        "bastion_secgroup_egress",
        direction="egress",
        ethertype="IPv4",
        remote_ip_prefix="0.0.0.0/0",
        security_group_id=bastion_secgroup.id,
    )

    # compute instance
    bastion = compute.Instance(
        "bastion",
        name="bastion",
        image_name=config.require("image_name"),
        flavor_name=config.require("flavor_bastion"),
        key_pair=cluster_keypair.name,
        security_groups=[secgroup, bastion_secgroup],
        networks=[compute.InstanceNetworkArgs(name=network_name)],
    )

    # and assign a floating IP
    compute.FloatingIpAssociate(
        "bastion",
        floating_ip=config.require("floating_ip_bastion"),
        instance_id=bastion.id,
    )


def worker():
    """
    Responsible for security group, its rules, compute instance and
    floating IP association for worker node(s).
    """

    # security group
    worker = networking.SecGroup(
        "worker",
        name="worker",
        description="Worker node",
        delete_default_rules=True,
    )

    # security group rules
    networking.SecGroupRule(
        "worker_secgroup_egress",
        direction="egress",
        ethertype="IPv4",
        remote_ip_prefix="0.0.0.0/0",
        security_group_id=worker.id,
    )

    # compute instance
    for i in range(0, config.require_int("number_of_workers")):
        compute.Instance(
            f"worker-{i}",
            name=f"worker-{i}",
            image_name=config.require("image_name"),
            flavor_name=config.require("flavor_worker"),
            key_pair=cluster_keypair.name,
            security_groups=[secgroup, worker],
            networks=[compute.InstanceNetworkArgs(name=network_name)],
        )


if __name__ == "__main__":
    bastion()
    worker()
