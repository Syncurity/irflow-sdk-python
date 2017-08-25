# Overview
This directory contains sample scripts intended to show how to use the
irflow_client.  These scripts will get you going very quickly.  The entire irflow-client API is 
used in the main script!  Look there for examples of any specific API Call

The contents of this directory are as follows:

1. Sample scripts
  * 01_run_all_api_calls.py - This script makes at least one call to each of the API functions.
  * 02_csv_to_alerts.py - This script reads a csv of fact data and creates one alert for each row 
  in the CSV (excluding the row of column headings).
  
2. Sample Files
  * sample_image.png - This image is uploaded as an attachment in one of the calls in 
  01_run_all_api_calls.py
  * sample_csv_of_alerts.csv - This is a file of data, with a header row at the top.  It is used 
  by 02_csv_to_alerts.py, and holds the data for the Alerts created by that script.
  
3. Configuration File
  * api.conf.template - This is a template file of the api.conf required to configure the 
  irflow_client.  It hold information about the IR Flow instance, and how to authenticate with 
  that instance, as well as instructing the irflow_client if it should print debugging information 
  to the console.
  
# Before You Get Started
Before you get started, there are a number of steps that you must take to prepare IR Flow for API 
calls, and configure the irflow_client so it can connect to your IR FLow instance.  Those steps 
are:

1. Prepare a IR Flow user, authorized to make API calls.
2. Whitelist the IP address that will be originating API calls to the IR Flow instance, in the IR 
Flow instance.
3. Create Alert Objects, and Data Source Configurations in the IR Flow instance to receive the data 
sent via the API Calls.
4. Create the Close Reason used by the script.
5. Configure the irflow_client library

#### Prepare a IR Flow user
The IR Flow REST API requires a username and a API Key associated with that user in order to 
authenticate the REST call.  In addition, the user must be a member of a group with API 
 Read/Write to the object type they are trying to access.
 
 The following steps create a user.
 
 1. Login to the IR Flow Web Application using an account with Admin privileges.
 2. Navigate to the Admin Panel
 3. Select the Users menu, and the Users Item on that menu.
 4. If an user account that you want to use already exists, click edit on that user.  If it does 
 not exist, create a user, and save it, then edit that new user.
 
 NOTE: IR Flow ships with a built in account named api, and a built in group named api.  The api 
 user is a member of the api group, and the api group has api read and write permissions.  This is 
 the normal user used for api calls, though there are plenty of use cases for creating 
 additional/different users with varying permissions.
 
 5. On the edit user screen, scroll to the API Key field.
 
 If the user already has an API Key, that is the value that must be placed in the api.conf 
 configuration file on the computer that will run the irflow_client library.  
 If the user does nto have an API Key, click generate to create an API Key.
 
 6. If the user is not a member of a group with API Read an Write (depending on the API operations 
 you intend to use), then add the appropriate group (i.e. one with API Read/Write to the object 
 you will be accessing).
 
 #### Whitelist the IP Address.
 IR Flow only allows API calls to be made from specific IP addresses.  These IP Addresses are 
 white listed inside the IR Flow Admin Panel.  do the following to white list your IP address.
 
 1. Determine the client machines IP address.  If you are unable to determine your client 
 computers IP Address, go ahead and execute an API Call against IR FLow.  IR Flow will create a 
 API Log entry showing the IP Address it has blocked.  You can find the API Log under the Admin 
 Panel -> API -> API Logs.  
 
 NOTE: The log screen is very wide sometimes, and you may need to scroll to the right to see the 
 IP Address.
 
 2. Go to the Admin Panel -> API -> API Whitelist.  Click Add, and Add the IP Address of th client 
 computer.
 
 #### Create Alert Objects, and Data Source Configurations in the IR Flow instance.
 
 In order to create an Alert through the REST API, you must have an Alert Object Type and 
 a Data Source Configuration.  The Data Source Configuration must specify the Alert Object Type as 
 the Object Type to use when creating the Alert.
 
 The 01_run_all_api_calls.py and 02_csv_to_alerts.py scripts assume that an Alert Object Type 
 named "Test Alert" with two fields:
 * Tier, as a string field.
 * Risk as an integer field.
 
 Both scripts also assume that a Data Source Configuration named 'ds_test' exists, and 
 specifies the "Test Alert" object type as the Data Source Configurations Alert Object Type.
 
 To configure this data in IR Flow, do the following:
 1. Log into the IR Flow Web Application.
 2. Select App Config --> Object Types on the main menu. This brings up the Object Types page.
 
 You see the four base object types listed, Alert, Incident, Task and Step.  These Object Types 
 can be extended in your IR Flow Instance, and new Object Types can be created that inherit from 
 the Base Object Types.
 
 We will create a new Object Type that inherits from the Alert Object Type.
 3. Press the "+" button nex to "Alert" on the left side of the Object Types screen.  This creates a new 
 Object Type, and names it new_type.
 4. On the right side of the screen, change the label to "Test Alert", and the name to "test_alert".
 5. Under the Fields section, click "New Field".
 6. Give the new field the label "Risk", the name "risk", and select the field type as Integer, then 
 Save the field.
 7. Do the same to create a field with label "Tier", name "tier", and type of "Test".  Save that field 
 as well.
 8. Select Data Flows --> Incoming Data and Triage on the main menu.  This brings up the "Incoming Data 
 Field Groups and Triage Steps" screen.
 9. Press the "+" Add button in the upper right corner.  This opens the Add a Data Source modal.
 10. Type in "ds_test" for the name, and select "Test Alert" from the Object Type drop down.
 11. Add another alert called "phishing" and select "Alert" from the Object Type drop down.
 12. Save the new Data Source.

 You have now configured IR Flow to accept the data as the python scripts send it.
 
 
 #### Create the "Close Reason" used by the script
 The 01_run_all_api_calls.py script uses a "Close Reason" to close the Alert after we create it and manipulate it a little.
 In order for the Close to work, that close reason must be defined in the IR Flow Instance.  To create the "Close Reason" do the following:
 1. Log into the IR Flow Web Application.
 2. Select App Config --> Close Reasons.
 3. Press the "Create" button on the upper right corner of the screen.
 4. Enter "Red Team Testing" for the name, fill in a description.
 5. Save the Close Reason.
 
 #### Add fields to Alert
 The 01_run_all_api_calls.py assumes the Alert object type will have two fields, "description" and "src_dns".
 Create them in the same way you created the Tier and Risk fields on Test Alert, but this time add them to the
 top level Alert.

 #### Configure the IR Flow Client library.

 The irflow_client needs to know some information in order to connect to your IR Flow instance.  This 
 includes the machine name/IP address of teh IR Flow instance, the IR FLow User, and the API Key for that user.
 
 To set-up the irflow_client you must create/edit the api.conf file in the examples directory.  
 A template is 
 provided for you named api.conf.template.  Make copy with the following command:

  ```
 > cp api.conf.template api.conf
  ```

 Your api.conf file is now the template with the following default values:

 ```buildoutcfg
[IRFlowAPI]
address=<irflow IP/hostname here>
api_user=<api username here>
api_key=<api key here>
debug=true
protocol=https
verbose = 1
```
Set the correct values for the address, user and API_key from your IR Flow instance.  If you do not 
know these values, see the instructions above.

There are two additional configurations you can change:
* debug:  If true the irflow_client prints debugging information to the console.  If false, no debugging information 
is printed to the console.

* verbose:  An integer 0 - 2.  
  * 0: REST Call data only:  URL, Body and Headers.
  * 1: Also print the HTTP Response Code.
  * 2: Also print the HTTP Response Json.
 # Running the test scripts
 
 The test scripts can run on any computer that has Python and the irflow_client installed.  
 irflow_client dependencies, which are installed automatically when the irflow_client is installed.
 
 To run the test scripts, go to a command prompt, navigate to the directory with your copy of the 
 test scripts, and enter the command
 ```
 > python 01_run_all_api_calls.py
```
or
```
> python 02_csv_to_alert.py
```

To see what the scripts are doing, go ahead and open them up.  There are plenty of comments intended 
to make clear what is happening in the script.
# A Couple of Comments about using the irflow_client
* The irflow_client is a python module, intended to be instantiated once, and used for multiple calls to 
the IR Flow REST API.  
* When the instance of the class is created, you pass irflow_client the path to 
the api.conf file, and the irflow_client uses that information for all connections.  
* You use the instantiated object to make calls to the IR Flow REST API without worrying about the headers, gets and put, 
and the details of the connection.
 
Happy Scripting!