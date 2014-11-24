from pyexperian import services


def test_address_street():
    address = {'city': 'austin', 'state': 'tx', 'zip': '78701', 'street1': 'first part', 'street2': 'second part'}
    translated = services.BaseProduct._translate_address(address)
    assert translated['Street'] == ("%s %s" % (address['street1'], address['street2']))

    address = {'city': 'austin', 'state': 'tx', 'zip': '78701', 'street1': 'first part', 'street2': 'second part', 'street': 'priority'}
    translated = services.BaseProduct._translate_address(address)
    assert translated['Street'] == address['street']

def test_good_business():
    business = {'name': 'Franklin BBQ', 'address': {'city': 'austin', 'state': 'tx', 'zip': '78701', 'street': ''}}
    translated = services.BaseProduct._translate_business(business)
    assert 'BusinessName' in translated
    assert 'CurrentAddress' in translated
    assert 'Street' not in translated['CurrentAddress'] and 'City' in translated['CurrentAddress'] and 'State' in translated['CurrentAddress'] and 'Zip' in translated['CurrentAddress']

def test_bools():
    assert services.BaseProduct._translate_to_bool(True) == 'Y'
    assert services.BaseProduct._translate_to_bool(False) == 'N'
    assert services.BaseProduct._translate_to_bool('y') == 'Y'
    assert services.BaseProduct._translate_to_bool('Y') == 'Y'
    assert services.BaseProduct._translate_to_bool('n') == 'N'
    assert services.BaseProduct._translate_to_bool('true') == 'Y'
    assert services.BaseProduct._translate_to_bool('false') == 'Y'
