#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_grant_endpoint

short_description: Grants permissions on endpoints of a SQL Server instance

description:
	- Grants permissions on endpoints of a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the endpoint
		required: true

	permission:
		description:
			- The permission to grant on the endpoint
		required: true

	principal:
		description:
			- The principal to grant the permission to
		required: true

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
# Grants CONNECT permission on the DBM endpoint named 'foo' to the login 'bar'
- mssql_endpoint:
	name: foo
	permission: CONNECT
	principal: bar
	login_name: sa
	login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the login that was added
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
			permission = dict(choices = ["CONNECT"], required = True),
			principal = dict(required = True),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		)
	)

	permission = module.params['permission']
	name = module.params['name']
	principal = module.params['principal']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	sqlcmd(login_port, login_name, login_password, """
		GRANT {0} ON ENDPOINT::{1} TO {2}
	""".format(
		permission,
		quoteName(name, '['),
		quoteName(principal, '[')
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
