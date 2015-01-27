from pyexperian import services, exceptions
from nose.tools import raises

try:
    from pyexperian.test import secrets

    ecals = services.Ecals(secrets.ECALS_URL)
    bpp = services.BusinessPremierProfile(secrets.config, ecals)
    sbcs = services.SBCS(secrets.config, ecals)
    bop = services.BusinessOwnerProfile(secrets.config, ecals)
except ImportError as e:
    ecals = bpp = sbcs = bop = None


@raises(exceptions.IncompleteBusinessException)
def test_empty_business():
    global bpp

    if not bpp:
        return

    bpp.query(business={})


@raises(exceptions.IncompleteBusinessException)
def test_no_business_address():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'Experian Information Solutions'
    }

    bpp.query(business=business)


@raises(exceptions.IncompleteBusinessException)
def test_incomplete_business_address():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'Experian Information Solutions',
        'address': {
            'state': 'CA',
            'zip': '92626'
        }
    }

    bpp.query(business=business)


def test_complete_business_address():
    global bpp

    if not bpp:
        return

    business = {
        'name': 'Experian Information Solutiosn',
        'address': {
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp = bpp.query(business=business)


    assert resp is not None


def test_complete_business_address_sbcs():
    global sbcs

    if not sbcs:
        return

    business = {
        'name': 'Experian Information Solutiosn',
        'address': {
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    resp = sbcs.query(business=business)


    assert resp is not None



@raises(exceptions.IncompleteOwnerException)
def test_empty_owner():
    global bop

    if not bop:
        return

    owner = {

    }

    bop.query(owner=owner)


@raises(exceptions.IncompleteOwnerException)
def test_incomplete_owner_name():
    global bop

    if not bop:
        return

    owner = {
        'last_name': 'Benson',
        'address': {
            'street': '7600 Trumbower Trl',
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    bop.query(owner=owner)



@raises(exceptions.IncompleteOwnerException)
def test_incomplete_address():
    global bop

    if not bop:
        return

    owner = {
        'first_name': 'Derrick',
        'last_name': 'Benson',
        'address': {
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    bop.query(owner=owner)


def test_complete_owner():
    global bop

    if not bop:
        return

    business = {
        'name': 'Experian Information Solutiosn',
        'address': {
            'city': 'Costa Mesa',
            'state': 'CA',
            'zip': '92626'
        }
    }

    owner = {
        'first_name': 'Derrick',
        'last_name': 'Benson',
        'address': {
            'street': '7600 Trumbower Trl',
            'city': 'Millington',
            'state': 'MI',
            'zip': '48746'
        }
    }

    resp = bop.query(business=business, owner=owner)


    assert resp is not None