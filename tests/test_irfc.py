import pytest

config_args = {
    'address': '50.19.169.130',
    'api_user': 'api',
    'api_key': '7ac832c355b1e6a840caaf9b6f96dc462fe003cc',
    'debug': True,
    'protocol': 'https'
}

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


@pytest.fixture
def irfc():
    from irflow_client import IRFlowClient
    return IRFlowClient(config_args)


def test_get_version(irfc):
    response = irfc.get_version()
    assert response == '4.6'


def test_create_alert(irfc):
    response = irfc.create_alert(proofpoint_message)
    assert response['success']
    assert response['exception'] is None
    assert response['errorCode'] is None
    assert 'Alert Created!' in response['message']
    assert isinstance(response['data']['alert'], dict)
    assert isinstance(response['data']['alert']['id'], int)
