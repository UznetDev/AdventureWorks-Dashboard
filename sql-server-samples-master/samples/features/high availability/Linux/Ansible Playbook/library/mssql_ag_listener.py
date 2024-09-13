#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_ag_listener

short_description: Create an availability group listener on a SQL Server instance

description:
	- Create an availability group listener on a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the listener to add
		required: true

	ag_name:
		description:
			- The name of the availability group to add the listener to
		required: true

	ip:
		description:
			- The IPs for the listener to bind to
		required: true

	readonly_routing_replicas:
		description:
			- A list of all the replicas of the AG that should participate in read-only routing
		required: false

	login_port:
		description:
			- The TDS port of the instance
		required: false
		default: 1433

	login_name:
		description:
			- The name of the user to log in to the instance
		required: true

	login_password:
		description:
			- The password of the user to log in to the instance
		required: true

notes:
	- Requires the mssql-tools package on the remote host.

requirements:
	- python >= 2.7
	- mssql-tools
'''.replace('\t', '  ')

EXAMPLES = '''
# Creates an AG listener named foo for the AG named bar with IP 1.2.3.4, and have all replicas in the "servers" group participate in read-only routing
- mssql_ag_listener:
	name: foo
	ag_name: bar
	ip:
		- '1.2.3.4'
	readonly_routing_replicas: "{{ groups['servers'] }}"
	login_name: sa
	login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the AG listener that was created
	returned: success
	type: string
	sample: foo
'''.replace('\t', '  ')


from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
	module = AnsibleModule(
		argument_spec = dict(
			name = dict(required = True),
			ag_name = dict(required = True),
			ip = dict(type = 'list', required = True),
			readonly_routing_replicas = dict(type = 'list', required = True),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		)
	)

	name = module.params['name']
	ag_name = module.params['ag_name']
	ips = module.params['ip']
	readonly_routing_replicas = module.params['readonly_routing_replicas']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	sqlcmd(login_port, login_name, login_password, """
		IF EXISTS (
			SELECT *
			FROM
				sys.availability_groups ag JOIN
				sys.availability_group_listeners agl ON ag.group_id = agl.group_id
			WHERE
				ag.name = {0} AND agl.dns_name = {2}
		)
			ALTER AVAILABILITY GROUP {1} REMOVE LISTENER {2}
		;

		ALTER AVAILABILITY GROUP {1} ADD LISTENER {2} (WITH IP ({3}))
	""".format(
		quoteName(ag_name, "'"),
		quoteName(ag_name, '['),
		quoteName(name, "'"),
		', '.join("({0}, '255.255.255.255')".format(quoteName(ip, "'")) for ip in ips)
	))

	for replica in readonly_routing_replicas:
		sqlcmd(login_port, login_name, login_password, """
			ALTER AVAILABILITY GROUP {0} MODIFY REPLICA ON {1} WITH (PRIMARY_ROLE (ALLOW_CONNECTIONS = READ_WRITE))
			;
			ALTER AVAILABILITY GROUP {0} MODIFY REPLICA ON {1} WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY))
			;
			ALTER AVAILABILITY GROUP {0} MODIFY REPLICA ON {1} WITH (SECONDARY_ROLE (READ_ONLY_ROUTING_URL = {2}))
			;
		""".format(
			quoteName(ag_name, '['),
			quoteName(replica.split('.')[0], "'"),
			quoteName('tcp://{0}:{1}'.format(replica, login_port), "'")
		))

	for replica in readonly_routing_replicas:
		sqlcmd(login_port, login_name, login_password, """
			ALTER AVAILABILITY GROUP {0} MODIFY REPLICA ON {1} WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = ({2})))
		""".format(
			quoteName(ag_name, '['),
			quoteName(replica.split('.')[0], "'"),
			', '.join(quoteName(other_replica.split('.')[0], "'") for other_replica in readonly_routing_replicas if other_replica != replica)
		))

	module.exit_json(changed = True, name = name)

def sqlcmd(login_port, login_name, login_password, command):
	subprocess.check_call([
		'/opt/mssql-tools/bin/sqlcmd',
		'-S',
		"localhost,{0}".format(login_port),
		'-U',
		login_name,
		'-P',
		login_password,
		'-b',
		'-Q',
		command
	])

def quoteName(name, quote_char):
	if quote_char == '[' or quote_char == ']':
		(quote_start_char, quote_end_char) = ('[', ']')
	elif quote_char == "'":
		(quote_start_char, quote_end_char) = ("N'", "'")
	else:
		raise Exception("Unsupported quote_char {0}, must be [ or ] or '".format(quote_char))

	return "{0}{1}{2}".format(quote_start_char, name.replace(quote_end_char, quote_end_char + quote_end_char), quote_end_char)

if __name__ == '__main__':
	main()
