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

    def __init__(self, config, ecals):
        self.config = config
        self.ecals = ecals

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

    # Pass in the entire NetConnectRequest XML
    def raw_query(self, xml):
        return self._post_xml(xml)

    # Helper function to simplify looking for a value nested deeply within a dictionary
    @classmethod
    def _get_dict_value(cls, d, key_list):
        if type(key_list) is not list:
            key_list = [key_list]

        for key in key_list:
            if type(key) == str and key in d:
                d = d[key]
            elif type(key) == int and len(d) >= key:
                d = d[key]
            else:
                return None

        return d

    @classmethod
    def _translate_addons(cls, addons_data={}):
        addons = {}

        # Include intelliscore
        if addons_data.get('score', None):
            addons['SCORE'] = addons_data['score']

        # Request owner profile only (BOP)
        if addons_data.get('stand_alone', None):
            addons['StandAlone'] = addons_data['stand_alone']

        # Request Business Profile with Intelliscore
        if addons_data.get('bp', None):
            addons['BP'] = addons_data['bp']

        # Return a list of similars
        if addons_data.get('list', None):
            addons['List'] = addons_data['list']

        return addons

    @classmethod
    def _translate_address(cls, address_data={}):
        address = {}

        if address_data.get('street', None):
            address['Street'] = address_data['street']
        elif address_data.get('street1', None):
            address['Street'] = "%s %s" % (address_data['street1'], address_data.get('street2', ''))

        if address_data.get('city', None):
            address['City'] = address_data['city']

        if address_data.get('state', None):
            address['State'] = address_data['state']

        if address_data.get('zip', None):
            address['Zip'] = address_data['zip']

        return address

    @classmethod
    def _translate_business(cls, business_data={}):
        business = {}

        if business_data.get('name', None):
            business['BusinessName'] = business_data['name']

        if business_data.get('alt_name', None):
            business['AlternateName'] = business_data['alt_name']

        if business_data.get('tax_id', None):
            business['TaxId'] = business_data['tax_id']

        if business_data.get('phone', None):
            business['Phone'] = {'Number': business_data['phone']}

        if business_data.get('address', None):
            business['CurrentAddress'] = cls._translate_address(business_data['address'])

        if business_data.get('bis_file_number', None):
            business['BISFileNumber'] = business_data['bis_file_number']

        if business_data.get('bis_list_number', None):
            business['BISListNumber'] = business_data['bis_list_number']

        return business

    @classmethod
    def _translate_owner(cls, owner_data={}):
        business_owner = {}

        owner_name = {}

        if owner_data.get('first_name', None):
            owner_name['First'] = owner_data['first_name']

        if owner_data.get('middle_name', None):
            owner_name['Middle'] = owner_data['middle_name']

        if owner_data.get('last_name', None):
            owner_name['Surname'] = owner_data['last_name']

        if owner_data.get('suffix', None):
            owner_name['Gen'] = owner_data['suffix']

        if owner_name:
            business_owner['OwnerName'] = owner_name

        if owner_data.get('ssn', None):
            business_owner['SSN'] = owner_data['ssn']

        if owner_data.get('age', None):
            business_owner['Age'] = owner_data['age']

        if owner_data.get('dob', None):
            business_owner['DOB'] = owner_data['dob']

        if owner_data.get('yob', None):
            business_owner['YOB'] = owner_data['yob']

        if owner_data.get('title', None):
            business_owner['Title'] = owner_data['title']

        if owner_data.get('address', None):
            business_owner['CurrentAddress'] = cls._translate_address(owner_data['address'])

        driver_license = {}
        if owner_data.get('driver_license_num', None):
            driver_license['Number'] = owner_data['driver_license_num']

        if owner_data.get('driver_license_state', None):
            driver_license['State'] = owner_data['driver_license_state']

        if driver_license:
            business_owner['DriverLicense'] = driver_license

        if owner_data.get('age', None):
            business_owner['Age'] = owner_data['age']

        return business_owner

    # Finalizes request data and converts to XML string.
    @classmethod
    def _to_xml(cls, data_dict={}):
        return dicttoxml.dicttoxml(data_dict, attr_type=False, custom_root='NetConnectRequest')

    @classmethod
    def _log_pretty_xml(cls, xml, _header=None):
        header = "\n======%s======\n" % _header.upper() if _header else "\n"
        logging.info("%s%s" % (header, parseString(xml).toprettyxml()))

    def _post_xml(self, xml):
        # Lock them out if too many bad auth attempts
        if BaseProduct.failed_auth_attempts >= constants.MAX_AUTH_ATTEMPTS:
            raise exceptions.MaxAuthAttemptsException()

        url = self.ecals.get_net_connect_url()

        self._log_pretty_xml(xml, 'request')

        logging.info("Net Connect URL: %s" % url)

        data = "NETCONNECT_TRANSACTION=%s" % (urllib.quote_plus(xml))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = (self.config['user_id'], self.config['user_pw'])

        response = requests.post(url, headers=headers, auth=auth, data=data)

        logging.info(response.text)

        if re.search('^<\?xml', response.text, re.IGNORECASE):
            self._log_pretty_xml(response.text, 'response')

            BaseProduct.failed_auth_attempts = 0

            response_dict = xmltodict.parse(response.text)['NetConnectResponse']

            if self._get_dict_value(response_dict, 'ErrorMessage') == 'Invalid request format':
                raise exceptions.BadRequestException()
            else:
                profile_type_code = self._get_dict_value(response_dict, ['Products', self.product_id, 'BusinessNameAndAddress', 'ProfileType', '@code'])
                if profile_type_code and profile_type_code.strip() == 'NO RECORD':
                    return None, response.text

        elif re.search('^<(!DOCTYPE )?html', response.text, re.IGNORECASE):

            # TODO using DEMO environment this is the only way to test for bad AUTH.
            if re.search('app\.logonUrl', response.text):
                BaseProduct.failed_auth_attempts += 1
                raise exceptions.FailedAuthException()

        return response_dict['Products'], response.text


class BusinessPremierProfile(BaseProduct):
    product_id = constants.BUSINESS_PREMIER_PROFILE_ID

    def query(self, business={}, owner={}, addons={}):
        request_data = self._get_base_request_data()

        defaults = {}

        request_data.update(defaults)

        if business:
            request_data['BusinessApplicant'] = self._translate_business(business)

        if addons:
            request_data['AddOns'] = self._translate_addons(addons)

        xml = self._to_xml(
            self._wrap_with_header({self.product_id: request_data}))

        return self._post_xml(xml)


class BusinessOwnerProfile(BaseProduct):
    product_id = constants.BUSINESS_OWNER_PROFILE_ID

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
            request_data['BusinessApplicant'] = self._translate_business(business)

        if owner:
            request_data['BusinessOwner'] = self._translate_owner(owner)

        if addons:
            request_data['AddOns'] = self._translate_addons(addons)

        xml = self._to_xml(
            self._wrap_with_header({self.product_id: request_data}))

        resp_dict, resp_xml = self._post_xml(xml)

        if self._get_dict_value(resp_dict, [self.product_id, 'ProcessingMessage', 'ProcessingAction', '@code']) == constants.TERMS_RESPONSE_CODE:
            raise exceptions.TermsException()

        return resp_dict, resp_xml


class SBCS(BaseProduct):
    product_id = constants.SBCS_ID

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
                'BusinessApplicant': self._translate_business(business)
            })

        if addons:
            request_data.update({
                'AddOns': self._translate_addons(addons)
            })

        xml = self._to_xml(
            self._wrap_with_header({self.product_id: request_data}))

        return self._post_xml(xml)


class Ecals():

    def __init__(self, ecals_url):
        self.ecals_url = ecals_url
        self.net_connect_url = (None, None)  # (url, time_pulled)

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

    @classmethod
    def is_valid_net_connect_url(cls, url):
        hostname = Ecals.get_hostname_from_url(url)
        return '.experian.com' in hostname

    # https://www.example.com/blog -> www.example.com
    @classmethod
    def get_hostname_from_url(cls, url):
        match = re.search(r'^https?://([^/]+).*$', url)
        return match.group(1) if match else None
