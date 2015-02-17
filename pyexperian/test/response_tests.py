from pyexperian import services, parsers, exceptions
from nose.tools import raises

try:
    from pyexperian.test import secrets

    ecals = services.Ecals(secrets.ECALS_URL)
    bpp = services.BusinessPremierProfile(secrets.config, ecals)
    sbcs = services.SBCS(secrets.config, ecals)
    bop = services.BusinessOwnerProfile(secrets.config, ecals)
    raw = services.Raw(secrets.config, ecals)
except ImportError as e:
    ecals = bpp = sbcs = bop = raw = None


def test_no_hit_premier_profile():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'NORECORDCO',
        'address': {
            'street': '123 Main Street',
            'city': 'Buena Park',
            'state': 'CA',
            'zip': '90620'
        }
    }

    bpp = services.BusinessPremierProfile(secrets.config, ecals)

    resp_blob = bpp.query(business=business)

    assert resp_blob is not None

    result = parsers.BusinessPremierProfile(resp_blob)

    assert not result.business_found()


def test_direct_hit_premier_profile():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '475 Anton Blvd',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp_blob = bpp.query(business=business)

    result = parsers.BusinessPremierProfile(resp_blob)

    assert not result.has_list()
    assert result.business_found()
    business_info = result.get_business()
    assert 'experian_bin' in business_info
    assert 'phone' in business_info
    assert 'address' in business_info

def test_list_of_similars_premier_profile():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'Experian',
        'address': {
            'street': '123 Main Street',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp_blob = bpp.query(business=business)

    result = parsers.BusinessPremierProfile(resp_blob)

    assert result.has_list()

    similars = result.get_list()

    assert len(similars) > 1


    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '123 Main Street',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp_blob = bpp.query(business=business)

    result = parsers.BusinessPremierProfile(resp_blob)

    assert result.has_list()
    similars = result.get_list()
    similar = similars[0]

    assert len(similars) == 1
    assert 'experian_bin' in similar
    assert 'name' in similar
    assert 'address' in similar

    business = {
        'experian_bin': similar['experian_bin']
    }

    resp_blob = bpp.query(business=business)

    result = parsers.BusinessPremierProfile(resp_blob)

    assert result.business_found()
    business = result.get_business()

    assert business['name'] == similar['name']


def test_standalone_business_owner_profile():
    global bop

    if not bop:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '475 Anton Blvd',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    owner = {
        'first_name': 'Derrick',
        'last_name': 'Benson',
        'ssn': '887487109',
        'address': {
            'street': '7600 Trumbower Trl',
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    resp_blob = bop.query(business=business, owner=owner)

    result = parsers.BusinessOwnerProfile(resp_blob)

    assert result.owner_found()


def test_extractor_match():
    global bop

    if not bop:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '475 Anton Blvd',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    owner = {
        'first_name': 'Derrick',
        'last_name': 'Benson',
        'ssn': '887487109',
        'address': {
            'street': '7600 Trumbower Trl',
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    resp_blob = bop.query(business=business, owner=owner)

    result = parsers.BusinessOwnerProfile(resp_blob)
    assert result.extract(['CreditProfile', 'RiskModel', 'Score']) == '0855'


def test_extractor_no_match():
    global bop

    if not bop:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '475 Anton Blvd',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    owner = {
        'first_name': 'Derrick',
        'last_name': 'Benson',
        'ssn': '887487109',
        'address': {
            'street': '7600 Trumbower Trl',
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    resp_blob = bop.query(business=business, owner=owner)

    result = parsers.BusinessOwnerProfile(resp_blob)
    assert result.extract(['Fake', 'Path', 'Score']) is None

def test_nohit_standalone_business_owner_profile():
    global bop

    if not bop:
        return

    business = {
        'name': 'Fake Biz',
        'phone': '999-555-1234',
        'address': {
            'street': 'Fake Addy',
            'city': 'Costa Fake',
            'state': 'CA',
            'zip': '78734'
        }
    }

    owner = {
        'first_name': 'Santa',
        'last_name': 'Jackson',
        'ssn': '999999999',
        'address': {
            'street': 'Fake Addy2',
            'city': 'Texas',
            'state': 'CA',
            'zip': '99911'
        }
    }

    resp_blob = bop.query(business=business, owner=owner)

    result = parsers.BusinessOwnerProfile(resp_blob)

    assert not result.business_found()
    assert not result.owner_found()

def test_no_hit_sbcs():
    global sbcs

    if not sbcs:
        return

    business = {
        'name': 'NORECORDCO',
        'address': {
            'street': '123 Main Street',
            'city': 'Buena Park',
            'state': 'CA',
            'zip': '90620'
        }
    }

    resp_blob = sbcs.query(business=business)

    result = parsers.SBCS(resp_blob)

    assert not result.business_found()


def test_direct_hit_sbcs():
    global sbcs

    if not sbcs:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '475 Anton Blvd',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }



    resp_blob = sbcs.query(business=business)

    result = parsers.SBCS(resp_blob)

    assert result.business_found()


def test_list_of_similars_sbcs():
    global sbcs

    if not sbcs:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'street': '123 Main Street',
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp_blob = sbcs.query(business=business)

    result = parsers.SBCS(resp_blob)

    assert result.has_list()


def test_raw_query():
    global raw

    if not raw:
        return

    xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <NetConnectRequest>
        <EAI>%(eai)s</EAI>
        <DBHost>%(db_host)s</DBHost>
        <Request xmlns="http://www.experian.com/WebDelivery" version="1.0">
            <Products>
                <PremierProfile>
                    <Subscriber>
                        <OpInitials>OP</OpInitials>
                        <SubCode>%(sub_code)s</SubCode>
                    </Subscriber>
                    <BusinessApplicant>
                        <BusinessName>EXPERIAN INFORMATION SOLUTIONS</BusinessName>
                        <CurrentAddress>
                            <Street>475 ANTON BLVD</Street>
                            <City>COSTA MESA</City>
                            <State>CA</State>
                            <Zip>92626</Zip>
                        </CurrentAddress>
                    </BusinessApplicant>
                    <OutputType>
                        <XML>
                            <Verbose>Y</Verbose>
                        </XML>
                    </OutputType>
                    <Vendor>
                        <VendorNumber>$(vendor_number)s</VendorNumber>
                    </Vendor>
                </PremierProfile>
            </Products>
        </Request>
    </NetConnectRequest>
    """ % {
            'eai': secrets.EAI,
            'db_host': secrets.DB_HOST,
            'sub_code': secrets.SUB_CODE,
            'vendor_number': secrets.VENDOR_NUMBER
        }

    result = raw.query(xml)

    assert result.index('NetConnectResponse') >= 0

@raises(exceptions.BadRequestException)
def test_bad_request_query():
    global raw

    if not raw:
        return

    xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <NetConnectRequest>
        <EAI>%(eai)s</EAI>
        <DBHost>%(db_host)s</DBHost>
        <Request xmlns="http://www.experian.com/WebDelivery" version="1.0">
            <Products>
                <PremierProfile>
                    <Subscriber>
                        <OpInitials>OP</OpInitials>
                        <SubCode>%(sub_code)s</SubCode>
                    </Subscriber>
                    <BusinessApplicant>
                        <BusinessName>EXPERIAN INFORMATION SOLUTIONS</BusinessName>
                        <CurrentAddress>
                            <Zip>92626</Zip>
                        </CurrentAddress>
                    </BusinessApplicant>
                    <OutputType>
                        <XML>
                            <Verbose>Y</Verbose>
                        </XML>
                    </OutputType>
                    <Vendor>
                        <VendorNumber>$(vendor_number)s</VendorNumber>
                    </Vendor>
                </PremierProfile>
            </Products>
        </Request>
    </NetConnectRequest>
    """ % {
            'eai': secrets.EAI,
            'db_host': secrets.DB_HOST,
            'sub_code': secrets.SUB_CODE,
            'vendor_number': secrets.VENDOR_NUMBER
        }

    result = raw.query(xml)

    parsed_result = parsers.BusinessPremierProfile(result)
