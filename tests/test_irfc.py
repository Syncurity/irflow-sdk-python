"""
    test_irfc.py. Pytests for irflow_client

    You must have test_data.py present in the tests directory to run tests successfully
"""
import pytest

from irflow_client import IRFlowClient

import test_data

# Test Client Setup Error handling
# def test_irfc_no_username():
#     """Test for missing username (api_user)"""
#     del config_args['api_user']
#
#     with pytest.raises(KeyError, message='Expecting no username error') as excinfo:
#         IRFlowClient(config_args=config_args)
#     exception_msg = excinfo.value.args[0]
#     assert exception_msg == 'api_user'

# Test data

config_args = test_data.config_args
config_args_missing_parameters = test_data.config_args_missing_parameters
config_args_to_try = test_data.config_args_to_try
proofpoint_message = test_data.proofpoint_message


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
    """
    Setup irflow_client instance
    :return:
        IRFlowClient
    """

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
