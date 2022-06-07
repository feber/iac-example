%{ if number_of_bastions == 1 }
Host bastion
  Hostname ${floating_ip_bastion}
  User ${ssh_user}
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  ControlMaster auto
  ControlPersist 5m
  IdentityFile ${private_key_path}

Host ${workers_name}
  IdentityFile ${private_key_path}
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  ProxyJump bastion
%{ endif }
