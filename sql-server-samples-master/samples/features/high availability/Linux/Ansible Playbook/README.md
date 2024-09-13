This is a sample Ansible playbook that shows how to install SQL Server, create a Pacemaker cluster, and create an AG managed by the cluster on a set of Linux nodes.


# Roles

- `pacemaker` - This role creates a Pacemaker cluster between the hosts.
- `mssql-server` - This role installs SQL Server on the host, runs setup to set the SA password, and starts the service.
- `mssql-server-ha` - This role enables support for HA and creates a DB Mirroring endpoint.
- `mssql-server-ag-external` - This role installs the Pacemaker resource agents, creates an AG, an optional listener, and Pacemaker resources for both.


# Try

1. Put the names of the Linux nodes in the `inventory` file

1. Configure the deployment in `play.yml`

1. Create a vault file named `vault.yml` using the template at the end of this README.

	```sh
	ansible-vault create vault.yml
	```

1. Execute the playbook

	```sh
	ansible-playbook ./play.yml -i ./inventory --ask-vault-pass -e 'ansible_user=username'
	```


# Vault file template

```yaml
---

ansible_ssh_pass: 'some password'

ansible_sudo_pass: 'some password'

# The password for the sa user. Only used if mssql-server needs to be installed.
sa_password: 'some password'

# The password for the master key
master_key_password: 'some password'

# The SQL password for the DBM endpoint user
dbm_password: 'some password'

# The password for the DBM cert private key
dbm_cert_password: 'some password'

# The password of the user that admins the pacemaker cluster (hacluster)
pacemaker_cluster_password: 'some password'

# The SQL password for the pacemaker user
pacemaker_password: 'some password'
```
