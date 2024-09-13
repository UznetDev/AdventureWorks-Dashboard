#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_user

short_description: Add users to a SQL Server instance

description:
	- Add ysers to a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the user to add
		required: true

	login:
		description:
			- The login name of the user to add
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
# Create a user named 'foo' for the login named 'bar'
- mssql_user:
		name: foo
		login: bar
		login_name: sa
		login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the user that was added
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
			login = dict(required = True),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		)
	)

	name = module.params['name']
	login = module.params['login']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	sqlcmd(login_port, login_name, login_password, """
		IF NOT EXISTS(
			SELECT * FROM sys.sysusers WHERE name = {0}
		)
			CREATE USER {1} FOR LOGIN {2}
		;
	""".format(
		quoteName(name, "'"),
		quoteName(name, '['),
		quoteName(login, '[')
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
