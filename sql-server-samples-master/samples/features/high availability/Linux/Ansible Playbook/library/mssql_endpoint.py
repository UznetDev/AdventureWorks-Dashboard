#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_login

short_description: Add endpoints to a SQL Server instance

description:
	- Add endpoints to a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the endpoint to add
		required: true

	ip:
		description:
			- The IP to bind to
		required: false
		default: 0.0.0.0

	port:
		description:
			- The port to bind to
		required: true

	type:
		description:
			- The type of the endpoint
		required: true
		choices: ["DATA_MIRRORING"]

	dbm_cert_name:
		description:
			- The name of the cert to use for the DATA_MIRRORING endpoint
		required: false
		default: []

	state:
		description:
			- The state to set the endpoint to
		required: false
		choices:
			- started
		default: started

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
# Create a DBM endpoint named 'foo' on port 5022 with authentication from the cert named 'bar'
- mssql_endpoint:
	name: foo
	port: 5022
	type: DATA_MIRRORING
	dbm_cert_name: bar
	state: started
	login_name: sa
	login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the endpoint that was added
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
			ip = dict(required = False, default = "0.0.0.0"),
			port = dict(required = True),
			type = dict(choices = ['DATA_MIRRORING'], required = True),
			dbm_cert_name = dict(required = False),
			state = dict(choices = ['started'], required = False, default = 'started'),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		),
		required_if = [
			['type', 'DATA_MIRRORING', ['dbm_cert_name']]
		]
	)

	name = module.params['name']
	ip = module.params['ip']
	port = module.params['port']
	type = module.params['type']
	dbm_cert_name = module.params['dbm_cert_name']
	state = module.params['state']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	if type == "DATA_MIRRORING":
		options = """
			ROLE = ALL,
			AUTHENTICATION = CERTIFICATE {0},
			ENCRYPTION = REQUIRED ALGORITHM AES
		""".format(
			quoteName(dbm_cert_name, '[')
		)

	sqlcmd(login_port, login_name, login_password, """
		IF NOT EXISTS(
			SELECT * FROM sys.tcp_endpoints WHERE name = {0}
		)
			CREATE ENDPOINT {1}
				AS TCP (LISTENER_IP = ({2}), LISTENER_PORT = {3})
				FOR DATA_MIRRORING ({4})
		;
	""".format(
		quoteName(name, "'"),
		quoteName(name, '['),
		ip,
		port,
		options
	))

	if state == 'started':
		sqlcmd(login_port, login_name, login_password, """
			IF NOT EXISTS(
				SELECT * FROM sys.tcp_endpoints WHERE name = {0} AND state = 0
			)
				ALTER ENDPOINT {1} STATE = STARTED
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
