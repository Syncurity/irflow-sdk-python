import json
import pytest

from irflow_client import IRFlowClient

config_args = {
    'address': '50.19.169.130',
    'api_user': 'api',
    'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
    'debug': True,
    'protocol': 'https'
}

config_args_missing_parameters = [
    {   # No API User key['api_user']
        'address': '50.19.169.130',
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    }, {   # No API Key key['api_key']
        'address': '50.19.169.130',
        'api_user': 'api',
        'debug': True,
        'protocol': 'https'
    }, {   # No API Server key['address']
        'api_user': 'api',
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    },
]

config_args_to_try = [
    {  # api_user = None
        'address': '50.19.169.130',
        'api_user': None,
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    }, {  # api_user = int
        'address': '50.19.169.130',
        'api_user': 123,
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    }, {  # api_user = list
        'address': '50.19.169.130',
        'api_user': ['abc', '123'],
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    }, {  # api_user = Bool
        'address': '50.19.169.130',
        'api_user': True,
        'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
        'debug': True,
        'protocol': 'https'
    },{  # api_key = None
        'address': '50.19.169.130',
        'api_user': 'api',
        'api_key': None,
        'debug': True,
        'protocol': 'https'
    }, {  # api_key = int
        'address': '50.19.169.130',
        'api_user': 'api',
        'api_key': 1,
        'debug': True,
        'protocol': 'https'
    },{  # api_key = list
        'address': '50.19.169.130',
        'api_user': 'api',
        'api_key': ['123', 'abc'],
        'debug': True,
        'protocol': 'https'
    }, {  # api_key = Bool
        'address': '50.19.169.130',
        'api_user': 'api',
        'api_key': True,
        'debug': True,
        'protocol': 'https'
    }
]

proofpoint_message = {
    "fields":
        {
            "emailTo": ["test@example.com"],
            "emailDate": "2017-07-21T01:06:05.000Z",
            "emailFrom": "=?utf-8?B?VS5TIEZlZGVyYWwgRmluYW5jaWFsIERlYnQgRGVwYXJ0bWVudA==?= ",
            "sourceAddress": "31.207.80.114", "emailSubject": "Collection of real estate",
            "deviceExternalId": "496568c0d9e7d8e8f9f74946a5e62dbde42944c27601ebcae26856ac646766a1",
            "originalAlertURL": "https:\/\/threatinsight.proofpoint.com\/302f9667-0366-df19-1c34-d02dd8ac4ab9\/threat\/email\/496568c0d9e7d8e8f9f74946a5e62dbde42944c27601ebcae26856ac646766a1",
            "category": "malware",
            "threatScores": [44, 0, 0]
        },
    "suppress_missing_field_warning": False,
    "description": "PyTest Proofpoint Messages Delivered",
    "data_field_group_name": "Proofpoint Messages Delivered"
}


# Test Client Setup Error handling
# def test_irfc_no_username():
#     """Test for missing username (api_user)"""
#     del config_args['api_user']
#
#     with pytest.raises(KeyError, message='Expecting no username error') as excinfo:
#         IRFlowClient(config_args=config_args)
#     exception_msg = excinfo.value.args[0]
#     assert exception_msg == 'api_user'


@pytest.fixture(params=config_args_to_try)
def config_args_generator(request):
    """Returns config_args_to_try"""
    return request.param


@pytest.fixture(params=config_args_missing_parameters)
def config_args_missing_params(request):
    """ Returns Missing Keys"""
    return request.param


def test_irfc_init_missing_param(config_args_missing_params):
    """Using config_args_missing_params fixture"""
    with pytest.raises(KeyError, message='Expecting no username error') as excinfo:
        response = IRFlowClient(config_args_missing_params)
    exception_msg = excinfo.typename
    assert exception_msg == 'KeyError'


def test_irfc_init(config_args_generator):
    """Using config_args_generator fixture"""
    # response = IRFlowClient(config_args_generator)
    with pytest.raises(KeyError, message='Expecting no username error') as excinfo:
        response = IRFlowClient(config_args_generator)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'You have the wrong or missing key or value'


@pytest.fixture(autouse=True)
def irfc():
    # Setup : start IRFlow Client

    return IRFlowClient(config_args)


def test_get_version(irfc):
    response = irfc.get_version()
    assert response == '4.6'


@pytest.mark.create_alert
def test_create_get_alert(irfc):
    # test that we an create an alert
    response = irfc.create_alert(proofpoint_message['fields'],
                                 proofpoint_message['description'],
                                 proofpoint_message['data_field_group_name'])
    assert response['success']
    assert response['exception'] is None
    assert response['errorCode'] is None
    assert 'Alert Created!' in response['message']
    assert isinstance(response['data']['alert'], dict)
    assert isinstance(response['data']['alert']['id'], int)

    alert_id = response['data']['alert']['id']
    next_response = irfc.get_alert(alert_num=alert_id)
    assert next_response['success']
    assert next_response['exception'] is None
    assert next_response['errorCode'] is None
    assert 'Alert found.' in next_response['message']
    assert isinstance(next_response['data']['alert'], dict)
    assert isinstance(next_response['data']['alert']['id'], int)
