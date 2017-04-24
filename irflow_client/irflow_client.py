import ConfigParser
from json import dumps
import pprint
import requests
import sys
import tempfile

# The next to lines suppress the SSL Warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class IRFlowClient(object):
    end_points = {
        'create_alert': 'api/v1/alerts.json',
        'get_alert': 'api/v1/alerts',
        'get_attachment': 'api/v1/attachments/%s/download',
        'put_attachment': 'api/v1/alerts/%s/attachments',
        'get_fact_group': 'api/v1/fact_groups',
        'put_fact_group': 'api/v1/fact_groups',
        'put_alert_close': 'api/v1/alerts/close',
    }

    def __init__(self, config_args=None, config_file=None):
        # Create a PrettyPrint object so we can dump JSon structures if debug = true.
        self.pp = pprint.PrettyPrinter(indent=4)

        # Make sure we have config info we need
        if not ( config_args or config_file ):
            print('Missing config input parameters. Need either api.conf, or to pass in config_args to'
                  'initialize IRFlowClient Class \n'
                  '')
        if config_args and config_file:
            print('!!! Warning !!! Since you provided both input args and an api.conf file, we are'
                  'defaulting to the input args.')

        # parse config_args dict
        if config_args:
            self._get_config_args_params(config_args)

        # Else parse api.conf
        elif config_file:
            self._get_config_file_params(config_file)

        # Get a reusable session object.
        self.session = requests.Session()
        # Set the X-Authorization header for all calls through the API
        # The rest of the headers are specified by the individual calls.
        self.session.headers.update({'X-Authorization': '{} {}'.format(self.api_user, self.api_key)})

    def _get_config_args_params(self, config_args):
        ''' gets args to setup a client connection
        
        Args:
            config_args (dict):
                Required:
                    "address":"IR-Flow Server FQDN or IP Address"
                    "api_user":"IR-Flow API User"
                    "api_key":"above user's api key"
                Optional
                    "protocol":"https unless otherwise specified"
                    "debug":"enable debug output, default = None"
                    "verbose":"turn up the verbosity"
        '''

        # Missing config checks done before class initializes in argparse

        self.address = config_args['address']
        self.api_user = config_args['api_user']
        self.api_key = config_args['api_key']
        if config_args['protocol']:
            self.protocol = config_args['protocol']
        else:
            self.protocol = 'https'
        if config_args['debug']:
            self.debug = config_args['debug']
        else:
            self.debug = False
        if config_args['verbose_level']:
            self.verbose = int(config_args['verbose_level'])
        else:
            self.verbose = 1

        # Dump Configuration if --debug
        if self.debug:
            self.dump_settings()

    def _get_config_file_params(self, config_file):

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
                'Configuration File "%s" does not contain the "address" option in the [IRFlowAPI] section'
                % config_file)
            missing_config = True
        if not config.has_option('IRFlowAPI', 'api_user'):
            print(
                'Configuration File "%s" does not contain the "api_user" option in the [IRFlowAPI] section'
                % config_file)
            missing_config = True
        if not config.has_option('IRFlowAPI', 'api_key'):
            print(
                'Configuration File "%s" does not contain the "api_key" option in the [IRFlowAPI] section'
                % config_file)
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
        if config.has_option('IRFlowAPI', 'verbose_level'):
            self.verbose = int(config.get('IRFlowAPI', 'verbose_level'))
        else:
            self.verbose = 1

        # Dump Configuration if --debug
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
        print('\tVerbose: "%s"' % self.verbose)

    def close_alert(self, alert_id, close_reason):
        url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['put_alert_close'])
        data = {"alert_num": "%s" % alert_id, "close_reason_name": "%s" % close_reason}
        headers = {'Content-type': 'application/json'}

        if self.debug:
            print('========== Close Alert ==========')
            print ('URL: "%s"' % url)
            print ('Body: "%s"' % data)
            print ('Session Headers: "%s"' % self.session.headers)
            print ('Headers: "%s"' % headers)

        response = self.session.put(url, json=data, headers=headers, verify=False)

        if self.debug:
            if self.verbose > 0:
                print('========== Close Alert Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())
        return response.json()

    def upload_attachment_to_alert(self, alert_id, filename):
        url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['put_attachment'])
        url = url % alert_id
        data = {'file': open(filename, 'rb')}
        headers = {}

        if self.debug:
            print ('========== Upload Attachment to Alert ==========')
            print ('URL: "%s"' % url)
            print ('Session Headers: "%s"' % self.session.headers)
            print ('Headers: "%s"' % headers)

        response = self.session.post(url, data={}, files=data, headers=headers, verify=False)

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())

        return response.json()

    def download_attachment(self, attachment_id, attachment_output_file):
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

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)

    def download_attachment_string(self, attachment_id):
        url = '%s://%s/%s' % (self.protocol, self.address, self.end_points['get_attachment'])
        url = url % attachment_id

        if self.debug:
            print ('========== Download Attachment ==========')
            print ('URL: "%s"' % url)
            print ('Session Headers: "%s"' % self.session.headers)
            print ('Headers: "%s"' % '')

        # Get a temporary file to download the results into
        temp = tempfile.TemporaryFile()

        response = self.session.get(url, stream=True, verify=False)
        # Iterate, downloading data 1,024 bytes at a time
        for block in response.iter_content(1024):
            temp.write(block)

        # Rewind the file to the beginning so we can read it into a string
        temp.seek(0)
        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)

        return temp.read()

    def put_fact_group(self, fact_group_id, fact_data):
        url = '%s://%s/%s/%s' % (self.protocol, self.address, self.end_points['get_fact_group'], fact_group_id)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        fact_payload = {'fields': fact_data}
        if self.debug:
            print ('========== PutFactGroup ==========')
            print ('URL: "%s"' % url)
            print ('Params: "%s"' % fact_payload)
            print ('Session Headers: "%s"' % self.session.headers)
            print ('Headers: "%s"' % headers)

        response = self.session.put(url, json=fact_payload, verify=False, headers=headers)

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())

        return response.json()

    def get_fact_group(self, fact_group_id):
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

        response = self.session.get(url, verify=False, headers=headers)

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())

        return response.json()

    def get_alert(self, alert_num):
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

        response = self.session.get(url, verify=False, headers=headers)

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())

        return response.json()

    def create_alert(self, alert_fields, description=None, incoming_field_group_name=None, alert_type_name=None):
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

        response = self.session.post(url, params=params, verify=False, headers=headers)

        if self.debug:
            if self.verbose > 0:
                print('========== Response ==========')
                print ('HTTP Status: "%s"' % response.status_code)
            if self.verbose > 1:
                print ('Response Json:')
                self.pp.pprint(response.json())

        return response.json()

    # The following helper functions are also defined in the irflow_client
    @staticmethod
    def get_field_by_name(field_name, field_list):
        for field in field_list:
            if field['field']['field_name'] == field_name:
                return field
        return None
