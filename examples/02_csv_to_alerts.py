import csv
import irflow_client

import pprint
from time import gmtime, strftime

pp = pprint.PrettyPrinter(indent = 4)

irflowAPI = irflow_client.IRFlowClient(config_file="./api.conf")
if irflowAPI.debug == "true":
	irflowAPI.dump_settings()

alert_type = 'ds_test'
description = 'New CSV Alert on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime())

with open('sample_csv_of_alerts.csv', 'rb') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		result = irflowAPI.create_alert(row, description = description, incoming_field_group_name = alert_type)
		if result['success']:
			print 'Created Alert_Num: ' + str(result['data']['alert']['alert_num'])
		else:
			print 'Failed to create alert'
			print 'Success == ' + str(result['success'])
			pp.pprint(result)
