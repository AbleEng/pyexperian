from pyexperian import services

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

    resp_dict, resp_blob = bpp.query(business=business)

    assert resp_dict is None


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


    resp_dict, resp_blob = bpp.query(business=business)

    assert resp_dict is not None
    assert 'ListOfSimilars' not in resp_dict[bpp.product_id]


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

    resp_dict, resp_blob = bpp.query(business=business)

    assert 'ListOfSimilars' in resp_dict[bpp.product_id]


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

    resp_dict, resp_blob = bop.query(business=business, owner=owner)

    assert resp_dict is not None


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

    sbcs = services.BusinessPremierProfile(secrets.config, ecals)

    resp_dict, resp_blob = sbcs.query(business=business)

    assert resp_dict is None


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


    resp_dict, resp_blob = sbcs.query(business=business)

    assert resp_dict is not None
    assert 'ListOfSimilars' not in resp_dict[sbcs.product_id]


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

    resp_dict, resp_blob = sbcs.query(business=business)

    assert 'ListOfSimilars' in resp_dict[sbcs.product_id]