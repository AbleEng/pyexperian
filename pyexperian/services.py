from pyexperian.lib import dicttoxml
from pyexperian import constants, exceptions
import requests
import xmltodict
import urllib
from xml.dom.minidom import parseString
import re
import time
import logging


def enable_debug(filename='pyexperian.log'):
    import datetime
    print('Debug mode is on. Events are logged at: %s' % filename)
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info('\nLogging session starts: %s' % (str(datetime.datetime.today())))


def disable_debug():
    logging.basicConfig(level=logging.WARNING)
    print('Debug mode is off.')


class BaseProduct():

    failed_auth_attempts = 0

    def __init__(self, config={}):
        self.config = config
        self.ecals = Ecals(config['ecals_url'])

    # Wrap the product data with request headers.
    def _wrap_with_header(self, product_data={}):
        return {
            'EAI': self.config['eai'],
            'DBHost': self.config['db_host'],
            'ReferenceId': self.config.get('reference_id', ''),
            'Request xmlns="http://www.experian.com/WebDelivery" version="1.0"': {
                'Products': product_data
            }
        }

    def _get_base_request_data(self):
        return {
            'Subscriber': {
                'OpInitials': self.config.get('op_initials', 'OP'),
                'SubCode': self.config['sub_code']
            },
            'OutputType': {
                'XML': {
                    'Verbose': 'Y'
                }
            },
            'Vendor': {
                'VendorNumber': self.config['vendor_number']
            }
        }

    @staticmethod
    def _translate_addons(addons_data={}):
        addons = {}

        # Return a list of similars
        if 'list' in addons_data:
            addons['List'] = 'Y' if addons_data.get('list').lower() == 'y' else 'N'

        # Include intelliscore
        if 'score' in addons_data:
            addons['SCORE'] = 'Y' if addons_data.get('score').lower() == 'y' else 'N'

        # Request owner profile only (BOP)
        if 'stand_alone' in addons_data:
            addons['StandAlone'] = 'Y' if addons_data.get('stand_alone').lower() == 'y' else 'N'

        # Request Business Profile with Intelliscore
        if 'bp' in addons_data:
            addons['BP'] = 'Y' if addons_data.get('bp').lower() == 'y' else 'N'

        if 'list' in addons_data:
            addons['List'] = 'Y' if addons_data.get('list').lower() == 'y' else 'N'

        return addons

    @staticmethod
    def _translate_address(address_data={}):
        address = {}
        if 'street' in address_data:
            address['Street'] = address_data['street']

        if 'city' in address_data:
            address['City'] = address_data['city']

        if 'state' in address_data:
            address['State'] = address_data['state']

        if 'zip' in address_data:
            address['Zip'] = address_data['zip']

        return address


    @staticmethod
    def _translate_business(business_data={}):
        business = {}
        if 'name' in business_data:
            business['BusinessName'] = business_data['name']

        if 'alt_name' in business_data:
            business['AlternateName'] = business_data['alt_name']

        if 'tax_id' in business_data:
            business['TaxId'] = business_data['tax_id']

        if 'phone' in business_data:
            business['Phone'] = {'Number': business_data['phone']}

        if 'address' in business_data:
            business['CurrentAddress'] = BaseProduct._translate_address(business_data['address'])

        return business

    @staticmethod
    def _translate_owner(owner_data={}):
        business_owner = {}

        owner_name = {}

        if 'first_name' in owner_data:
            owner_name['First'] = owner_data['first_name']

        if 'middle_name' in owner_data:
            owner_name['Middle'] = owner_data['middle_name']

        if 'last_name' in owner_data:
            owner_name['Surname'] = owner_data['last_name']

        if 'suffix' in owner_data:
            owner_name['Gen'] = owner_data['suffix']

        if owner_name:
            business_owner['OwnerName'] = owner_name

        if 'ssn' in owner_data:
            business_owner['SSN'] = owner_data['ssn']

        if 'age' in owner_data:
            business_owner['Age'] = owner_data['age']

        if 'dob' in owner_data:
            business_owner['DOB'] = owner_data['dob']

        if 'yob' in owner_data:
            business_owner['YOB'] = owner_data['yob']

        if 'title' in owner_data:
            business_owner['Title'] = owner_data['title']

        if 'address' in owner_data:
            business_owner['CurrentAddress'] = BaseProduct._translate_address(owner_data['address'])

        driver_license = {}
        if 'driver_license_num' in owner_data:
            driver_license['Number'] = owner_data['driver_license_num']

        if 'driver_license_state' in owner_data:
            driver_license['State'] = owner_data['driver_license_state']

        if driver_license:
            business_owner['DriverLicense'] = driver_license

        if 'age' in owner_data:
            business_owner['Age'] = owner_data['age']

        return business_owner

    @staticmethod
    # Finalizes request data and converts to XML string.
    def _to_xml(data_dict={}):
        return dicttoxml.dicttoxml(data_dict, attr_type=False, custom_root='NetConnectRequest')

    @staticmethod
    def _log_pretty_xml(xml, _header=None):
        header = "\n======%s======\n" % _header.upper() if _header else "\n"
        logging.info("%s%s" % (header, parseString(xml).toprettyxml()))

    def _post_xml(self, xml=''):
        # Lock them out if too many bad auth attempts
        if self.failed_auth_attempts >= constants.MAX_AUTH_ATTEMPTS:
            raise exceptions.MaxAuthAttemptsException()

        url = self.ecals.get_net_connect_url()

        BaseProduct._log_pretty_xml(xml, 'request')

        logging.info("Net Connect URL: %s" % url)

        data = "NETCONNECT_TRANSACTION=%s" % (urllib.quote_plus(xml))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = (self.config['user_id'], self.config['user_pw'])

        response = requests.post(url, headers=headers, auth=auth, data=data)

        BaseProduct._log_pretty_xml(response.text, 'response')

        # TODO using DEMO environment this is the only way to test for bad AUTH.
        if re.search('<!DOCTYPE html', response.text):
            self.failed_auth_attempts += 1
            raise exceptions.FailedAuthException()
        else:
            self.failed_auth_attempts = 0

        response_dict = xmltodict.parse(response.text)['NetConnectResponse']

        if 'ErrorMessage' in response_dict and response_dict['ErrorMessage'] == 'Invalid request format':
            raise exceptions.ConfigException()

        return response


class BusinessPremierProfile(BaseProduct):

    def query(self, business={}, owner={}, addons={}):
        request_data = self._get_base_request_data()

        defaults = {}

        request_data.update(defaults)

        if business:
            request_data['BusinessApplicant'] = BaseProduct._translate_business(business)

        if addons:
            request_data['AddOns'] = BaseProduct._translate_addons(addons)

        xml = BaseProduct._to_xml(
            self._wrap_with_header({'PremierProfile': request_data}))

        return self._post_xml(xml)


class BusinessOwnerProfile(BaseProduct):

    def query(self, business={}, owner={}, addons={}):
        request_data = self._get_base_request_data()

        defaults = {
            'AddOns': {
                'StandAlone': 'Y'
            }
        }

        if owner:
            # TODO
            defaults['Options'] = {'CustomerName': 'CustomerName'}

        request_data.update(defaults)

        if business:
            request_data['BusinessApplicant'] = BaseProduct._translate_business(business)

        if owner:
            request_data['BusinessOwner'] = BaseProduct._translate_owner(owner)

        if addons:
            request_data['AddOns'] = BaseProduct._translate_addons(addons)

        xml = BaseProduct._to_xml(
            self._wrap_with_header({'BusinessProfile': request_data}))

        return self._post_xml(xml)


class SBCS(BaseProduct):

    def query(self, business={}, addons={}, owner={}):
        request_data = self._get_base_request_data()

        defaults = {
            'AddOns': {
                'SCORE': 'Y',
                'BP': 'Y'
            }
        }

        request_data.update(defaults)

        if business:
            request_data.update({
                'BusinessApplicant': BaseProduct._translate_business(business)
            })

        if addons:
            request_data.update({
                'AddOns': BaseProduct._translate_addons(addons)
            })

        xml = BaseProduct._to_xml(
            self._wrap_with_header({'SmallBusinessCreditShare': request_data}))

        return self._post_xml(xml)


class Ecals():

    net_connect_url = (None, None)  # (url, time_pulled)

    def __init__(self, ecals_url):
        self.ecals_url = ecals_url

    def get_net_connect_url(self):
        # Check if Net Connect URL is expired.
        last_time_pulled = self.net_connect_url[1]
        if not last_time_pulled or ((time.time() - last_time_pulled) >= constants.URL_EXPIRATION_IN_SECONDS):
            logging.info("Net Connect URL is absent or expired.")
            self.net_connect_url = (self._fetch_net_connect_url(), time.time())

        return self.net_connect_url[0]

    def _fetch_net_connect_url(self):
        logging.info("Fetching new Net Connect URL from ECALS.")
        response = requests.get(self.ecals_url)
        if response.status_code == constants.HTTP_STATUS_OK:
            net_connect_url = response.text
            if Ecals.is_valid_net_connect_url(net_connect_url):
                return net_connect_url
            else:
                raise exceptions.InvalidNetConnectUrlException()
        else:
            raise exceptions.EcalsLookupException()

    @staticmethod
    def is_valid_net_connect_url(url):
        hostname = Ecals.get_hostname_from_url(url)
        return '.experian.com' in hostname

    # https://www.example.com/blog -> www.example.com
    @staticmethod
    def get_hostname_from_url(url):
        match = re.search(r'^https?://([^/]+).*$', url)
        return match.group(1) if match else None