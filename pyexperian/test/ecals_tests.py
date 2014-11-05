from pyexperian import services


def test_get_hostname_from_url():
    assert services.Ecals.get_hostname_from_url('https://www.google.com/blog') == 'www.google.com'
    assert services.Ecals.get_hostname_from_url('http://candy-crush.blah-3.org') == 'candy-crush.blah-3.org'
    assert services.Ecals.get_hostname_from_url('candy-crush.blah') is None


def test_net_connect_url():
    assert not services.Ecals.is_valid_net_connect_url('https://experian.fake.com')
    assert not services.Ecals.is_valid_net_connect_url('https://experian.org')
    assert services.Ecals.is_valid_net_connect_url('https://dm1.experian.com/netconnect2_0Demo/servlets/NetConnectServlet')


def test_fetch_net_connect_url():
    ecals = services.Ecals("http://www.experian.com/lookupServlet1?lookupServiceName=AccessPoint&lookupServiceVersion=1.0&serviceName=NetConnectDemo&serviceVersion=2.0&responseType=text/plain")
    assert ecals.get_net_connect_url() is not None
