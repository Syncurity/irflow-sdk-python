# Import the irflow_client module.
import irflow_client

# library used to create a unique value to pass to an IR Flow fact.
import uuid

# The first thing any script does is instantiate the irflow_api client library.
# NOTE: We pass the configuration file to the library when we instatiate it.
# The configuration file specifies the
# irflow end point, user, and API Key, as well as the debug flag.

irflowAPI = irflow_client.IRFlowClient("./api.conf")
if irflowAPI.debug == "true":
	irflowAPI.dump_settings()

print ('========== Create Alert ==========')
# Create an Alert using the API
# First set-up the alert data we want to use to create this alert with.
alert_fields = {'Tier': 'Tier1', 'Risk': 3}
description = 'Super Bad API Event'  # The Alert Description
# Note this matches the Data Source Configuration name in IR Flow.
# You will get an error if this DS Config does not exist in IR Flow.
ds_config_name = 'ds_test'
# Call the irflow_api method to create an alert.
# NOTE: irflowAPI is the object we created from the irflow_client.  This is how all methods are called.
# The call returns a json data structure (a dictionary in python)
alert_data = irflowAPI.create_alert(alert_fields, description=description, incoming_field_group_name=ds_config_name)

# Now get the alert_num (The unique id used to interact with this alert through the REST API.
# You can use this alert_num to go fetch ALL the data about an alert using the REST API
alert_num = alert_data['data']['alert_num']

if alert_data['success']:
	print "Create Alert: Success"
	print "Created Alert_Num: " + str(alert_num)
else:
	print "Create Alert: Failed"

print ('========== Get Alert ==========')
# Now go grab the event we just created and get all its data as a json structure,
# then grab its create_at value and print it.
new_alert = irflowAPI.get_alert(alert_num)

if alert_data['success']:
	print "Get Alert: Success"
	print 'Alert_Num:' + str(new_alert['data']['alert']['alert_num'])
	# Grab the created_at field
	created_at = new_alert['data']['alert']['created_at']

	print 'Created_at:' + created_at
else:
	print "Get Alert: Failed"

print ('========== Get Fact Group ==========')


fact_group_id = new_alert['data']['alert']['fact_group_id']
fact_data = irflowAPI.get_fact_group(fact_group_id)

if fact_data['success']:
	print "Get Fact Group: Success"
	facts = fact_data['data']['fact_group']['facts']  # List of the facts

	print 'Tier:' + str(irflowAPI.get_field_by_name('Tier', facts)['value'])
	print 'Risk:' + str(irflowAPI.get_field_by_name('Risk', facts)['value'])
else:
	print "Get Fact Group: Failed"

print ('========== Put Fact Group ==========')
# Now Update the Tier Field
# We are going to overwrite the original value of the Tier field with a new GUID.
new_value = uuid.uuid4()
new_fact_data = {'Tier': '%s' % new_value, 'Risk': 1}
# In order to update Facts on a Alert, we have to retrieve the fact_group_id from the Alert.
# Note that this call is going to override the original values we set in the create_alert call above.
update_results = irflowAPI.put_fact_group(fact_group_id, new_fact_data)

if update_results['success'] == True:
	print "Update Fact Group: Success"
	print "Updated Tier to: '%s'" % new_value
else:
	print "Update Fact Group: Failed"

print ('========== Get Fact Group to See Changed Value ==========')

fact_data = irflowAPI.get_fact_group(fact_group_id)

if fact_data['success']:
	print "Get Fact Group: Success"
	facts = fact_data['data']['fact_group']['facts']  # List of the facts

	print 'Tier:' + str(irflowAPI.get_field_by_name('Tier', facts)['value'])
	print 'Should match Value put to fact group above ^^^^^'
else:
	print "Get Fact Group: Failed"

print ('========== Upload Attachment To Alert ==========')
# Now upload a file to the Alert
# This image is our test image.  It should appear as an attachment to the Alert.
upload_result = irflowAPI.upload_attachment_to_alert(alert_num, "./sample_image.png")

if fact_data['success']:
	print "Upload Attachment to Alert: Success"
else:
	print "Upload Attachment to Alert: Failed"



print ('========== Download Attachment ==========')
# Now we need to fetch the Alert Data again, so we can grab the Attachment_id of the attachment we just uploaded,
# and use it to download the attachment.
alert_data = irflowAPI.get_alert(alert_num)

# Note that we know there is only one attachment because we just created the alert, then uploaded a single file.
# If we were worknig with an arbitrary alert in the application, we might need to search through the
# list of attachments to find the right on by name.
attachment_id = alert_data['data']['alert']['attachments'][0]['id']
# Download the image to a new file.  They better be the same image!
irflowAPI.download_attachment(attachment_id, './downloaded_sample_image.png')

print ('========== Close Alert ==========')
# This first call should return success = failure, as we do not hae a close reason "Foo Bar", unless you added one!
close_response = irflowAPI.close_alert(alert_num, "Foo Bar")
if close_response['success'] == False:
	print "Close Alert with Close Reason = 'Foo Bar' failed as expected."
else:
	print "Close Alert with Close Reason = 'Foo Bar' succeeded.  This was not expected!"
# This is the close reason we added in the set-up!
close_response = irflowAPI.close_alert(alert_num, "Red Team Testing")
if close_response['success'] == True:
	print "Close Alert with Close Reason = 'Red Team Testing' succeeded as expected."
else:
	print "Close Alert with Close Reason = 'Red Team Testing' failed.  This was not expected!"
