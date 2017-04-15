#!/usr/bin/python

import sys
import irflow_client
import pprint
import uuid

pp = pprint.PrettyPrinter(indent = 4)

# Rename External Module from irflow_api -> irflow_client v1.0

irflowAPI = irflow_client.IRFlowApi("api.conf")
if irflowAPI.debug == "true":
	irflowAPI.Dump()

# Create an Alert using the API
alert_fields = {'fqdn': 'bettersafety.net'}
description = 'Super Bad API Event'
incoming_field_group_name = 'ds_test'
alert_data = irflowAPI.CreateAlert(alert_fields, description=description, incoming_field_group_name=incoming_field_group_name)

print ('===== Response =====')
pp.pprint(alert_data)

alert_num = alert_data['data']['alert_num']

print ('===== Alert Number =====')
print "Created Alert_Num: " + str(alert_num)

# Now go grab the event we just created and dump its created_at to the console
new_alert = irflowAPI.GetAlert(alert_num)

print ('===== Response =====')
pp.pprint(new_alert)
print ('===== Alert Number =====')
print 'Fetched Alert_Num:' + str(new_alert['data']['alert']['alert_num'])

# Grab the created_at field
created_at = new_alert['data']['alert']['created_at']

print 'The fetched alert created at is:'
print created_at

print
print "The fetched response data is:"
pp.pprint(new_alert)

# Now add a fact field with a GUID Value that can be checked against the retrieved value
new_value = uuid.uuid4()

fact_group_id = new_alert['data']['alert']['fact_group_id']

fact_data = irflowAPI.GetFactGroup(fact_group_id)
print
print "The facts for the Alert"
pp.pprint(fact_data)

# Now Update the Tier Field
new_fact_data = {'Tier': 'Tier1', 'Risk': 1,}
update_results = irflowAPI.PutFactGroup(fact_group_id, new_fact_data)

print
print "Updating Facts Results:"
pp.pprint(update_results)
# print "Fact Update Success: " + update_results['']

print ('========== Preparing to script attachments ===================')
alert_64 = irflowAPI.GetAlert(64)
print "Fetch Alert Num: 64 to grab its attachment"
pp.pprint(alert_64)

attachment_id = alert_64['data']['alert']['attachments'][0]['id']
irflowAPI.DownloadAttachment(attachment_id, './attachment.txt')

# Now upload a file to the Alert
upload_result = irflowAPI.UploadAttachmentToAlert(64, "./SOC Dashboard - 2017-01-27.png")

print "===================="
print "Upload Results"
pp.pprint(upload_result)
# Go check the alert to see if it has the attachment as of NOW.
