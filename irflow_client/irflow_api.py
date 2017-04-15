import requests
import ConfigParser
import sys
from json import dumps
import argparse
from pprint import pprint as pp
import re


# TODO
# import logging
# logger = logging.getLogger('irflow-alert')

class IRFlowApi(object):
	"""IR-Flow api
	Class that wraps the IR-Flow REST API.
	"""

	end_points = {
		'create_alert': 'api/v1/alerts.json',
		'get_alert': 'api/v1/alerts',
		'get_attachment': 'api/v1/attachments/%s/download',
		'put_attachment': 'api/v1/alerts/%s/attachments',
		'get_fact_group': 'api/v1/fact_groups',
		'put_fact_group': 'api/v1/fact_groups'
	}

	def __init__(self, config_file):
		"""
		Initialize IRFlow Alert Api

		Arguments:
			config_file {str} -- [Relative or Absolute pointer to the API.conf file that configures the API]

		Keyword Arguments:
		"""

		config = ConfigParser.ConfigParser()
		config.read(config_file)

		# Make sure the Config File has the IRFlowAPI Section
		if not config.has_section('IRFlowAPI'):
			print 'Config file "%s" does not have the required section "[IRFlowAPI]"' % config_file
			sys.exit()

		missing_config = False
		# Check for missing required configuration keys
		if not config.has_option('IRFlowAPI', 'address'):
			print(
				'Configuration File "%s" does not contain the "address" option in the [IRFlowAPI] section' % config_file)
			missing_config = True
		if not config.has_option('IRFlowAPI', 'api_user'):
			print(
				'Configuration File "%s" does not contain the "api_user" option in the [IRFlowAPI] section' % config_file)
			missing_config = True
		if not config.has_option('IRFlowAPI', 'api_key'):
			print(
				'Configuration File "%s" does not contain the "api_user" option in the [IRFlowAPI] section' % config_file)
			missing_config = True

		# Do not need to check for protocol, it is optional.  Will assume https if missing.
		# Do not need to check for debug, it is optional.  Will assume False if missing.

		# If the required keys do not exist, then simply exit
		if missing_config:
			sys.exit()

		# Now set the configuration values on the self object.
		self.address = config.get('IRFlowAPI', 'address')
		self.api_user = config.get('IRFlowAPI', 'api_user')
		self.api_key = config.get('IRFlowAPI', 'api_key')
		if config.has_option('IRFlowAPI', 'protocol'):
			self.protocol = config.get('IRFlowAPI', 'protocol')
		else:
			self.protocol = 'https'
		if config.has_option('IRFlowAPI', 'debug'):
			self.debug = config.getboolean('IRFlowAPI', 'debug')
		else:
			self.debug = False

		# Get a reusable session object.
		self.session = requests.Session()
		# Set the X-Authorization header for all calls through the API
		# The rest of the heders are specified by the individual calls.
		self.session.headers.update({'X-Authorization': '{} {}'.format(self.api_user, self.api_key)})

		if self.debug:
			self.dump_settings()

	def dump_settings(self):
		print ('========== IRFlowAPI Created ==========')
		print ('Configuration Settings:')
		print ('\tAddress: "%s"' % self.address)
		print ('\tAPI_User: "%s"' % self.api_user)
		print ('\tAPI_Key: "%s"' % self.api_key)
		print ('\tProtocol: "%s"' % self.protocol)
		print ('\tDebug: "%s"' % self.debug)

	def UploadAttachmentToAlert(self, alert_id, filename):
		url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['put_attachment'])
		url = url % alert_id
		data = {'file': open(filename, 'rb')}
		# headers = {'Content-type': 'multipart/form-data'}
		headers = {}

		if self.debug:
			print ('========== Upload Attachment to Alert ==========')
			print ('URL: "%s"' % url)
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % headers)

		response = self.session.post(url, data={}, files=data, headers=headers, verify=False)

		print response
		return response.json()

	def DownloadAttachment(self, attachment_id, attachment_output_file):
		url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['get_attachment'])
		url = url % attachment_id

		if self.debug:
			print ('========== Download Attachment ==========')
			print ('URL: "%s"' % url)
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % '')

		with open(attachment_output_file, 'wb') as handle:
			response = self.session.get(url, stream=True, verify=False)
			for block in response.iter_content(1024):
				handle.write(block)

	def PutFactGroup(self, fact_group_id, fact_data):
		url = '%s://%s/%s/%s' % (self.protocol, self.address, self.end_points['get_fact_group'], fact_group_id)
		headers = {
			'Content-type': 'application/json',
			'Accept': 'application/json'
		}
		if self.debug:
			print ('========== PutFactGroup ==========')
			print ('URL: "%s"' % url)
			print ('Params: "%s"' % fact_data)
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % headers)
		return self.session.get(url, json=fact_data, verify=False, headers=headers).json()

	def GetFactGroup(self, fact_group_id):
		url = '%s://%s/%s/%s' % (self.protocol, self.address, self.end_points['get_fact_group'], fact_group_id)
		headers = {
			'Content-type': 'application/json',
			'Accept': 'application/json'
		}
		if self.debug:
			print ('========== GetFactGroup ==========')
			print ('URL: "%s"' % url)
			print ('Params: ""')
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % headers)
		return self.session.get(url, verify=False, headers=headers).json()

	def GetAlert(self, alert_num):
		url = '%s://%s/%s/%s' % (self.protocol, self.address, self.end_points['get_alert'], alert_num)
		headers = {
			'Content-type': 'application/json',
			'Accept': 'application/json'
		}
		if self.debug:
			print ('========== GetAlert ==========')
			print ('URL: "%s"' % url)
			print ('Params: ""')
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % headers)
		return self.session.get(url, verify=False, headers=headers).json()

	def CreateAlert(self, alert_fields, description=None, incoming_field_group_name=None, alert_type_name=None):
		"""Create an alert in IR-Flow

		CreateAlert allows you to easily create

		Arguments:
			alert_fields {dict} -- [description]

		Keyword Arguments:
			alert_desc {str} -- [description] (default: {None})
			incoming_field_group_name {str} -- [description] (default: {None})
			alert_type_name {str} -- [description] (default: {None})

		Returns:
			dict -- Alsways contains success={bool}. 
				On success contains alert_id={int}.
				On error contains error_message={str} and http_code={int}

		"""
		url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['create_alert'])
		params = {
			'text': dumps(alert_fields),
		}
		headers = {
			'Content-type': 'application/json',
			'Accept': 'application/json'
		}

		if description is not None:
			params['description'] = description
		if incoming_field_group_name is not None:
			params['data_field_group_name'] = incoming_field_group_name
		elif alert_type_name is not None:
			params['alert_type_name'] = alert_type_name

		if self.debug:
			print ('========== CreateAlert ==========')
			print ('URL: "%s"' % url)
			print ('Params: %s' % params)
			print ('Session Headers: "%s"' % self.session.headers)
			print ('Headers: "%s"' % headers)
		return self.session.post(url, params=params, verify=False, headers=headers).json()

	def __PostURL(self, params):
		"""Post to a url

		HTTP Post


		Arguments:
			params {dict} -- URL Parameters to use

		Returns:
			{dict}
		"""
		r = self.session.post(self.base_url, params=params, verify=False)
		# self.log.debug('Request URL: {}'.format(r.url))
		return self.__CheckResponse(r.json(), r.status_code)

	def __CheckResponse(self, ret_json, status_code):
		"""Check if our alert was created

		Check if our alert was created

		Arguments:
			ret_json {dict} -- Response data from post
			status_code {int} -- HTTP Status code

		Returns:
			{dict} 
		"""

		ret = {
			'success': ret_json['success'],
		}

		if ret['success']:
			match = self.regex.match(ret_json['message'])
			ret['alert_id'] = int(match.group(1))
		# self.log.debug('Created alert with id: {}'.format(match.group(1)))
		else:
			ret['http_code'] = status_code
			# self.log.error('IR-Flow response HTTP Status Code: {}'.format(status_code))

			ret['error_message'] = ret_json['message']
			# self.log.error('IR-Flow return error message: {}'.format(ret_json['message']))
			if ret_json['errorCode'] is not None:
				ret['error_code'] = ret_json['errorCode']
			# self.log.error('IR-Flow response error code: {}'.format(ret_json['errorCode']))
		return ret


def GetCmdArgs():
	"""CMD argument parser

	Command line argument parser for testing and examples

	Returns:
		{argparse.Namespace} -- Parsed options to be sent to class during initialization. 
	"""
	parser = argparse.ArgumentParser(description='Create a new alert in IR-Flow.')
	parser.add_argument('-a', '--address', dest='address', required=True, action='store', help='IR-Flow hostname/IP.')
	parser.add_argument('-u', '--api_user', dest='api_user', required=True, action='store', help='IR-Flow API Username')
	parser.add_argument('-k', '--api_key', dest='api_key', required=True, action='store', help='IR-Flow API Key')
	parser.add_argument('-p', '--protocol', dest='protocol', choices=['http', 'https'], default='https',
						help='Use http instead of https.')
	parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enable debug logging.')
	# parser.add_argument('-t', '--test', dest='test', action='store_true', help='Output results even if none.')
	options = parser.parse_args()
	return options


if __name__ == '__main__':
	args = GetCmdArgs()

	irflow = IRFlowAlertApi(**vars(args))
	alert_fields = {'fqdn': 'bettersafety.net'}
	desc = 'Super Bad API Alert'
	incoming_field_group_name = 'API - Test'
	print irflow.CreateAlert(alert_fields, alert_desc=desc, incoming_field_group_name=incoming_field_group_name)
