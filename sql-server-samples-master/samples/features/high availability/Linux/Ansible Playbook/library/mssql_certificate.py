#!/usr/bin/python

# Copyright (c) 2017 Microsoft Corporation

ANSIBLE_METADATA = {
	'metadata_version': '1.1',
	'supported_by': 'community',
	'status': ['preview']
}

DOCUMENTATION = '''
---
module: mssql_certificate

short_description: Add certificates to a SQL Server instance

description:
	- Add certificates to a SQL Server instance.

version_added: "2.2"

author: Arnav Singh (@arsing)

options:
	name:
		description:
			- The name of the certificate to add
		required: true

	authorization_username:
		description:
			- The name of the SQL user to authorize with this certificate
		required: false
		default: 0.0.0.0

	pub_key_path:
		description:
			- The path of the public key of the certificate (in Windows form)
		required: true

	priv_key_path:
		description:
			- The path of the private key of the certificate (in Windows form)
		required: true

	priv_key_password:
		description:
			- The password to decrypt the private key of the certificate
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
- mssql_certificate:
	name: dbm_cert
	authorization_username: dbm_user
	pub_key_path: "C:\\var\\opt\\mssql\\secrets\\dbm_certificate.cer"
	priv_key_path: "C:\\var\\opt\\mssql\\secrets\\dbm_certificate.pvk"
	priv_key_password: password
	login_name: sa
	login_password: password
'''.replace('\t', '  ')

RETURN = '''
name:
	description: The name of the certificate that was added
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
			authorization_username = dict(required = True),
			pub_key_path = dict(required = True),
			priv_key_path = dict(required = True),
			priv_key_password = dict(required = True, no_log = True),
			login_port = dict(required = False, default = 1433),
			login_name = dict(required = True),
			login_password = dict(required = True, no_log = True)
		)
	)

	name = module.params['name']
	authorization_username = module.params['authorization_username']
	pub_key_path = module.params['pub_key_path']
	priv_key_path = module.params['priv_key_path']
	priv_key_password = module.params['priv_key_password']
	login_port = module.params['login_port']
	login_name = module.params['login_name']
	login_password = module.params['login_password']

	sqlcmd(login_port, login_name, login_password, """
		IF NOT EXISTS(
			SELECT * FROM sys.certificates WHERE name = {0}
		)
			CREATE CERTIFICATE {1}
				AUTHORIZATION {2}
				FROM FILE = {3}
				WITH PRIVATE KEY (
					FILE = {4},
					DECRYPTION BY PASSWORD = {5}
				)
		;
	""".format(
		quoteName(name, "'"),
		quoteName(name, '['),
		quoteName(authorization_username, '['),
		quoteName(pub_key_path, "'"),
		quoteName(priv_key_path, "'"),
		quoteName(priv_key_password, "'")
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
