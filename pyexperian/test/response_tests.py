from pyexperian import services, parsers

try:
    from pyexperian.test import secrets

    ecals = services.Ecals(secrets.EXPERIAN_ECALS_URL)
    bpp = services.BusinessPremierProfile(secrets.config, ecals)
    sbcs = services.SBCS(secrets.config, ecals)
    bop = services.BusinessOwnerProfile(secrets.config, ecals)
except ImportError as e:
    ecals = bpp = sbcs = bop = None


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

def test_list_of_similars_premier_profile():
    global bpp

    if not bpp:
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

    resp_blob = bpp.query(business=business)

    result = parsers.BusinessPremierProfile(resp_blob)

    assert result.has_list()

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

def test_nohit_standalone_business_owner_profile():
    global bop

    if not bop:
        return

    business = {
        'name': 'Fake Biz',
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

