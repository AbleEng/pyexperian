# These tests verify the Experian authentication exam.

from pyexperian import services, exceptions
from nose.tools import raises, with_setup
import requests
import re


config = {}


def setup():
    # These values don't matter since exceptions are thrown before we get passed SSL
    config['user_id'] = 'USER_ID'
    config['user_pw'] = 'USER_PW'
    config['eai'] = 'EAI'
    config['vendor_number'] = 'VENDOR_NUMBER'
    config['sub_code'] = 'SUB_CODE'
    config['db_host'] = 'DB_HOST'
    config['test_subcode'] ='TEST_SUBCODE'


def teardown():
    for key in config.items():
        config[key] = None


@with_setup(setup, teardown)
@raises(exceptions.InvalidNetConnectUrlException)
def test_auth_case_1():
    _ecals = services.Ecals("http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnect&serviceVersion=0.1&responseType=text/plain")
    _ecals.get_net_connect_url()

@with_setup(setup, teardown)
def test_auth_case_2():
    ecals = services.Ecals('http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnect&serviceVersion=0.2&responseType=text/plain')
    bpp = services.BusinessPremierProfile(config, ecals);

    try:
        bpp.query(business={'name': 'norecordco', 'address':{'street': '123 main street', 'city': 'buena park', 'state': 'CA', 'zip': '90620'}})
    except requests.exceptions.SSLError as e:
        assert re.search("hostname .* doesn't match", str(e)) is not None


@with_setup(setup, teardown)
def test_auth_case_3():
    ecals = services.Ecals('http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnect&serviceVersion=0.3&responseType=text/plain')
    bpp = services.BusinessPremierProfile(config, ecals)

    try:
        bpp.query(business={'name': 'norecordco', 'address': {'street': '123 main street', 'city': 'buena park', 'state': 'CA', 'zip': '90620'}})
    except requests.exceptions.SSLError as e:
        assert re.search('certificate verify failed', str(e)) is not None


@with_setup(setup, teardown)
@raises(requests.exceptions.ConnectionError)
def test_auth_case_4():
    ecals = services.Ecals('http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnect&serviceVersion=0.4&responseType=text/plain')
    bpp = services.BusinessPremierProfile(config, ecals)

    bpp.query(business={'name': 'norecordco', 'address': {'street': '123 main street', 'city': 'buena park', 'state': 'CA', 'zip': '90620'}})