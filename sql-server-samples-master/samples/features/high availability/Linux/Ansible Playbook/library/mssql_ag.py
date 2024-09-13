#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_ag

short_description: Add or join availability groups on a SQL Server instance

description:
	- Add or join availability groups on a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the availability group to add
		required: true

	state:
		description:
			- The state to set the local replica to
		choices: ["all_secondaries_or_unjoined", "all_joined_to_one_primary"]
		required: true

	all_replicas:
		description:
			- A list of all the replicas of the AG
		required: false

	primary:
		description:
			- The replica that should become the primary
		required: false

	local_replica:
		description:
			- The name of the local replica
		required: false

	dbm_endpoint_port:
		description:
			- The port of the DBM endpoint
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
# Set all replicas of AG foo to secondary
- mssql_ag:
	name: foo
	state: all_secondaries_or_unjoined
	login_name: sa
	login_password: password

# Join all replicas of AG foo to primary on the first server in the group named servers
- mssql_ag:
	name: foo
	state: all_joined_to_one_primary
	all_replicas: "{{ groups['servers'] }}"
	primary: "{{ groups['servers'][0] }}"
	local_replica: "{{ inventory_hostname }}"
	login_name: sa
	login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the AG that was created or joined
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
			state = dict(choices = ['all_secondaries_or_unjoined', 'all_joined_to_one_primary'], required = True),
			all_replicas = dict(type = 'list', required = False),
			primary = dict(required = False),
			local_replica = dict(required = False),
			dbm_endpoint_port = dict(required = False),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		),
		required_if = [
			['state', 'all_joined_to_one_primary', ['all_replicas', 'primary', 'local_replica', 'dbm_endpoint_port']]
		]
	)

	name = module.params['name']
	state = module.params['state']
	all_replicas = module.params['all_replicas']
	primary = module.params['primary']
	local_replica = module.params['local_replica']
	dbm_endpoint_port = module.params['dbm_endpoint_port']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	if state == "all_secondaries_or_unjoined":
		sqlcmd(login_port, login_name, login_password, """
			IF EXISTS (
				SELECT * FROM sys.availability_groups WHERE name = {0}
			)
				ALTER AVAILABILITY GROUP {1} SET (ROLE = SECONDARY)
			;
		""".format(
			quoteName(name, "'"),
			quoteName(name, '[')
		))

	elif primary == local_replica:
		def replica_spec(name, endpoint_port):
			return """
				{0} WITH (
					ENDPOINT_URL = {1},
					AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
					FAILOVER_MODE = EXTERNAL,
					SEEDING_MODE = AUTOMATIC
				)
			""".format(
				quoteName(name.split('.')[0], "'"),
				quoteName('tcp://{0}:{1}'.format(name, endpoint_port), "'")
			)

		sqlcmd(login_port, login_name, login_password, """
			IF NOT EXISTS (
				SELECT * FROM sys.availability_groups WHERE name = {0}
			)
				CREATE AVAILABILITY GROUP {1}
					WITH (CLUSTER_TYPE = EXTERNAL, DB_FAILOVER = ON)
					FOR REPLICA ON {2}
			ELSE IF NOT EXISTS (
				SELECT *
				FROM sys.dm_hadr_availability_replica_states ars
				JOIN sys.availability_groups ag ON ars.group_id = ag.group_id
				WHERE ag.name = {0} AND ars.is_local = 1 AND ars.role = 1
			)
				BEGIN
				EXEC sp_set_session_context @key = N'external_cluster', @value = N'yes', @read_only = 1
				ALTER AVAILABILITY GROUP {1} FAILOVER
				END
			;

			ALTER AVAILABILITY GROUP {1} GRANT CREATE ANY DATABASE
			;
		""".format(
			quoteName(name, "'"),
			quoteName(name, '['),
			replica_spec(primary, dbm_endpoint_port)
		))

		for replica in all_replicas:
			if replica != primary:
				sqlcmd(login_port, login_name, login_password, """
					IF NOT EXISTS (
						SELECT *
						FROM sys.availability_replicas ar
						JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
						WHERE ag.name = {0} AND ar.replica_server_name = {2}
					)
						ALTER AVAILABILITY GROUP {1}
							ADD REPLICA ON {3}
					;
				""".format(
					quoteName(name, "'"),
					quoteName(name, '['),
					quoteName(replica.split('.')[0], "'"),
					replica_spec(replica, dbm_endpoint_port)
				))

	else:
		sqlcmd(login_port, login_name, login_password, """
			IF NOT EXISTS (
				SELECT * FROM sys.availability_groups WHERE name = {0}
			)
				ALTER AVAILABILITY GROUP {1} JOIN WITH (CLUSTER_TYPE = EXTERNAL)
			;

			ALTER AVAILABILITY GROUP {1} GRANT CREATE ANY DATABASE
			;
		""".format(
			quoteName(name, "'"),
			quoteName(name, '[')
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
