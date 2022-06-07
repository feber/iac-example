[bastion]
bastion-1 ansible_host=${floating_ip_bastion}

[worker]
%{for host in workers~}
${host.name} ansible_host=${host.access_ip_v4}
%{endfor~}

[worker:vars]
ansible_ssh_common_args='%{ if number_of_bastions == 1 }-F ssh-bastion.cfg%{ endif }'

[all:vars]
ansible_user=${ssh_user}
ansible_ssh_private_key_file=${private_key_path}
