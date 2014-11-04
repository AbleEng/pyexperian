from pyexperian.pyexperian import Ecals


def test_get_hostname_from_url():
    assert Ecals.get_hostname_from_url('https://www.google.com/blog') == 'www.google.com'
    assert Ecals.get_hostname_from_url('http://candy-crush.blah-3.org') == 'candy-crush.blah-3.org'
    assert Ecals.get_hostname_from_url('candy-crush.blah') is None


def test_net_connect_url():
    assert not Ecals.is_valid_net_connect_url('https://experian.fake.com')
    assert not Ecals.is_valid_net_connect_url('https://experian.org')
    assert Ecals.is_valid_net_connect_url('https://dm1.experian.com/netconnect2_0Demo/servlets/NetConnectServlet')


def test_fetch_net_connect_url():
    lookup = Ecals("http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnectDemo&serviceVersion=2.0&responseType=text/plain")
    assert lookup.get_net_connect_url() is not None
