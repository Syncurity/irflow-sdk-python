# Import the irflow_client module.
import irflow_client

# library used to create a unique value to pass to an IR Flow fact.
import uuid

# library used to generate a datetime
import datetime

# library to used print json in a readable format
import pprint

# The first thing any script does is instantiate the irflow_api client library.
# NOTE: We pass the configuration file to the library when we instatiate it.
# The configuration file specifies the
# irflow end point, user, and API Key, as well as the debug flag.

irflowAPI = irflow_client.IRFlowClient(config_file="./api.conf")
if irflowAPI.debug == "true":
    irflowAPI.dump_settings()

print ('========== Create Object Type ==========')
object_type = irflowAPI.create_object_type(type_name="createdByApi6", type_label="CreatedByAPi6", parent_type_name="alert")
if object_type['success']:
    print("Created object_type with id" + str(object_type['data']['object_type']['id']))
else:
    print("Failed to create object type")


print ('========== Attach Field to Object Type ==========')
attach_field = irflowAPI.attach_field_to_object_type('createdByApi6', 'av_detected')
if attach_field['success']:
    print("Attached field av_detected")
else:
    print("Failed to attach field av_detected")

print ('========== Create Alert ==========')
# Create an Alert using the API
# First set-up the alert data we want to use to create this alert with.
alert_fields = {'src_dns': 'phish.com', 'description': 'A description of the phish.'}
description = 'Super Bad API Event'  # The Alert Description
# Note this matches the Data Source Configuration name in IR Flow.
# You will get an error if this DS Config does not exist in IR Flow.
ds_config_name = 'Phishing'
# Call the irflow_api method to create an alert.
# NOTE: irflowAPI is the object we created from the irflow_client.  This is how all methods are called.
# The call returns a json data structure (a dictionary in python)
alert_data = irflowAPI.create_alert(alert_fields, description=description, incoming_field_group_name=ds_config_name)

if alert_data['success']:
    # Now get the alert_num (The unique id used to interact with this alert through the REST API.
    # You can use this alert_num to go fetch ALL the data about an alert using the REST API
    alert_num = alert_data['data']['alert']['alert_num']
    print("Create Alert: Success")
    print("Created Alert_Num: " + str(alert_num))
else:
    print("Create Alert: Failed")

print('========== Get Alert ==========')
# Now go grab the alert we just created and get all its data as a json structure,
# then grab its create_at value and print it.
new_alert = irflowAPI.get_alert(alert_num)

if new_alert['success']:
    print("Get Alert: Success")
    print('Alert_Num: ' + str(new_alert['data']['alert']['alert_num']))
    # Grab the created_at field
    created_at = new_alert['data']['alert']['created_at']

    print('Created_at: ' + created_at)
else:
    print("Get Alert: Failed")

# print('========== Get Fact Group ==========')
#
#
fact_group_id = new_alert['data']['alert']['fact_group_id']
fact_data = irflowAPI.get_fact_group(fact_group_id)
#
if fact_data['success']:
    print("Get Fact Group: Success")
    facts = fact_data['data']['fact_group']['facts']  # List of the facts

    print('Source DNS: ' + str(irflowAPI.get_field_by_name('src_dns', facts)['value']))
    print('Description: ' + str(irflowAPI.get_field_by_name('description', facts)['value']))
else:
    print("Get Fact Group: Failed")

print('========== Put Fact Group ==========')
# Now Update the Source DNS Field
# We are going to overwrite the original value of the Source DNS field with a new GUID.
new_value = 'phishing.com'
new_fact_data = {'src_dns': new_value, 'file_hash': '%s' % uuid.uuid4()}
# In order to update Facts on a Alert, we have to retrieve the fact_group_id from the Alert.
# Note that this call is going to override the original values we set in the create_alert call above.
update_results = irflowAPI.put_fact_group(fact_group_id, new_fact_data)

if update_results['success']:
    print("Update Fact Group: Success")
    print("Updated Source DNS to: '%s'" % new_value)
else:
    print("Update Fact Group: Failed")

print('========== Get Fact Group to See Changed Value ==========')

fact_data = irflowAPI.get_fact_group(fact_group_id)

if fact_data['success']:
    print("Get Fact Group: Success")
    facts = fact_data['data']['fact_group']['facts']  # List of the facts

    print('Source DNS: ' + str(irflowAPI.get_field_by_name('src_dns', facts)['value']))
    print('Should match Value put to fact group above ^^^^^')
else:
    print("Get Fact Group: Failed")

print('========== Upload Attachment To Alert ==========')
# Now upload a file to the Alert
# This image is our test image.  It should appear as an attachment to the Alert.
upload_result = irflowAPI.upload_attachment_to_alert(alert_num, "./sample_image.png")

if upload_result['success']:
    print("Upload Attachment to Alert: Success")
else:
    print("Upload Attachment to Alert: Failed")


print('========== Download Attachment ==========')
# Now we need to fetch the Alert Data again, so we can grab the Attachment_id of the attachment we just uploaded,
# and use it to download the attachment.
alert_data = irflowAPI.get_alert(alert_num)

# Note that we know there is only one attachment because we just created the alert, then uploaded a single file.
# If we were worknig with an arbitrary alert in the application, we might need to search through the
# list of attachments to find the right on by name.
attachment_id = alert_data['data']['alert']['attachments'][0]['id']
# Download the image to a new file.  They better be the same image!
irflowAPI.download_attachment(attachment_id, './downloaded_sample_image.png')

print('========== Close Alert ==========')
# This first call should return success = failure, as we do not hae a close reason "Foo Bar", unless you added one!
close_response = irflowAPI.close_alert(alert_num, "Foo Bar")
if close_response['success']:
    print("Close Alert with Close Reason = 'Foo Bar' succeeded.  This was not expected!")
else:
    print("Close Alert with Close Reason = 'Foo Bar' failed as expected.")

# This is the close reason we added in the set-up!
close_response = irflowAPI.close_alert(alert_num, "Red Team Testing")
if close_response['success']:
    print("Close Alert with Close Reason = 'Red Team Testing' succeeded as expected.")
else:
    print("Close Alert with Close Reason = 'Red Team Testing' failed.  This was not expected!")


print('========== Create Incident ==========')
# Create an Incident using the API
# First set-up the Incident data we want to use to create this Incident with.
incident_fields = {'time_contained': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
description = 'Super Bad API Incident'  # The Alert Description
# Note this matches the Incident Type name in IR Flow.
# You will get an error if this Incident Type does not exist in IR Flow.
incident_type_name = 'Phishing'
incident_subtype_name = 'Inbound Phishing'
# Call the irflow_api method to create an Incident.
# NOTE: irflowAPI is the object we created from the irflow_client.  This is how all methods are called.
# The call returns a json data structure (a dictionary in python)
incident_data = irflowAPI.create_incident(incident_fields,
                                          incident_type_name,
                                          incident_subtype_name=incident_subtype_name,
                                          description=description)

# Now get the incident_num (The unique id used to interact with this Incident through the REST API.
# You can use this incident_num to go fetch ALL the data about an Incident using the REST API
incident_num = incident_data['data']['incident']['incident_num']

if incident_data['success']:
    print("Create Incident: Success")
    print("Created Incident_Num: " + str(incident_num))
else:
    print("Create Incident: Failed")


print('========== Get Incident ==========')
# Now go grab the Incident we just created and get all its data as a json structure,
# then grab its create_at value and print it.
get_incident_result = irflowAPI.get_incident(incident_num)

if get_incident_result['success']:
    print("Get Incident: Success")
    print('Incident_Num: ' + str(get_incident_result['data']['incident']['incident_num']))
    # Grab the created_at field
    created_at = get_incident_result['data']['incident']['created_at']

    print('Created_at: ' + created_at)
else:
    print("Get Incident: Failed")


print('========== Attach Alert to Incident ==========')
# Attach the Alert created to the new Incident
attach_alert_result = irflowAPI.attach_alert_to_incident(alert_num, incident_num)

if attach_alert_result['success']:
    print("Attach Alert to Incident: Success")
else:
    print("Attach Alert to Incident: Failed")


print('========== Update Incident ==========')
# Update an Incident using the API
# Update set-up the Incident data we want to use to update this Incident.
incident_fields = {'time_remediated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
description = 'Super Bad API Incident - Remediated'  # The Alert Description
# Call the irflow_api method to update an Incident.
# NOTE: irflowAPI is the object we created from the irflow_client.  This is how all methods are called.
# The call returns a json data structure (a dictionary in python)
incident_data = irflowAPI.update_incident(incident_num, incident_fields, incident_type_name, incident_subtype_name=incident_subtype_name, description=description)

if incident_data['success']:
    print("Update Incident: Success")
else:
    print("Update Incident: Failed")


print('========== Upload Attachment To Incident ==========')
# Now upload a file to the Incident
# This image is our test image.  It should appear as an attachment to the Incident.
upload_result = irflowAPI.upload_attachment_to_incident(incident_num, "./sample_image.png")

if upload_result['success']:
    print("Upload Attachment to Incident: Success")
else:
    print("Upload Attachment to Incident: Failed")


def test_picklist_apis(found_picklist):
    picklist_id = found_picklist['id']

    # Get the Picklist the was just found
    print('========== Get Picklist ==========')
    picklist_data = irflowAPI.get_picklist(picklist_id)

    if picklist_data['success']:
        print("Get Picklist: Success")
        print('Picklist: ' + str(picklist_data['data']['picklist']['name']))
    else:
        print ("Get Picklist: Failed")

    # Add an item to the Picklist
    print('========== Add Item to Picklist ==========')
    add_item_result = irflowAPI.add_item_to_picklist(picklist_id, 'example_value', 'Example Label')

    if add_item_result['success']:
        picklist_item_id = add_item_result['data']['picklist_item']['id']
        print("Add Item to Picklist: Success")
        print('Picklist Item ID: ' + str(picklist_item_id))
    else:
        print("Add Item to Picklist: Failed")

    # Get the Picklist Item that was just created
    print('========== Get Picklist Item ==========')
    picklist_item_data = irflowAPI.get_picklist_item(picklist_item_id)

    if picklist_item_data['success']:
        print("Get Picklist Item: Success")
        print('Picklist Item: ' + str(picklist_item_data['data']['picklist_item']['label']))
    else:
        print("Get Picklist Item: Failed")

    # Delete the Picklist Item that was just created
    print('========== Delete Picklist Item ==========')
    delete_item_result = irflowAPI.delete_picklist_item(picklist_item_id)

    if delete_item_result['success']:
        print("Delete Picklist Item: Success")
    else:
        print("Delete Picklist Item: Failed")

    # Create a duplicate Picklist Item with this picklist_id
    print('========== Create Picklist Item ==========')
    create_item_result = irflowAPI.create_picklist_item(picklist_id, 'example_value', 'Example Label')

    if create_item_result['success']:
        print("Add Item to Picklist: Succeeded unexpected. Something went wrong.")
    else:
        print("Add Item to Picklist: Failed as expected. Can't add a duplicate picklist item.")

    # Get a list of the deleted picklists
    print('========== List of Deleted Picklist Items ==========')
    list_deleted_result = irflowAPI.list_picklist_items(picklist_id, only_trashed=True)

    if list_deleted_result['success']:
        print("List Picklist Items: Success")
    else:
        print("List Picklist Items: Failed")

    # Restore the Picklist Item that was just deleted
    print('========== Restore Picklist Item ==========')
    restore_item_result = irflowAPI.restore_picklist_item(picklist_item_id)

    if restore_item_result['success']:
        print("Restore Picklist Item: Success")
    else:
        print("Restore Picklist Item: Failed")


print('========== Get List of Picklists ==========')
picklists_result = irflowAPI.list_picklists()

if picklists_result['success']:
    print("List Picklists: Success")
else:
    print("List Picklists: Failed")

# Check if any picklists were found
if 'picklists' in picklists_result['data']:
    # Find the picklist with the name "New Picklist"
    picklist_name = 'New Picklist'
    found_picklist = False
    for picklist in picklists_result['data']['picklists']:
        if picklist['name'] == picklist_name:
            found_picklist = picklist
            break  # Break the loop once the picklist is found

if found_picklist:
    test_picklist_apis(found_picklist)
