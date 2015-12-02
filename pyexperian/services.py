from pyexperian.lib import dicttoxml
from pyexperian import constants, exceptions, session
from xml.dom.minidom import parseString
import urllib
import re
import time
import logging


class NetConnect():
    failed_auth_attempts = 0

    def __init__(self, config):
        self.config = config
        self.ecals = Ecals(self.config['ecals_url'])

    def build(self, product_id, query_data):
        request_data = self._get_base_request_data()
        request_data.update(query_data)

        return _dict_to_xml(self._wrap_request_with_header({product_id: request_data}), 'NetConnectRequest')

    def execute(self, request_xml, **kwargs):
        return self._post_xml(request_xml, **kwargs)

    def query(self, product_id, query_data, **kwargs):
        self.execute(self.build(product_id, query_data), **kwargs)

    def _wrap_request_with_header(self, product_data):
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

    def _post_xml(self, xml, **kwargs):
        # Lock them out if too many bad auth attempts
        if NetConnect.failed_auth_attempts >= constants.MAX_AUTH_ATTEMPTS:
            raise exceptions.MaxAuthAttemptsException()

        url = self.ecals.get_net_connect_url()

        _log_pretty_xml(xml, 'request')

        logging.info("Net Connect URL: %s" % url)

        data = "NETCONNECT_TRANSACTION=%s" % (urllib.quote_plus(xml))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = (self.config['user_id'], self.config['user_pw'])

        response = session.get_session().post(url, headers=headers, auth=auth, data=data, **kwargs)

        logging.info(response.text)

        if re.search('^<\?xml', response.text, re.IGNORECASE):
            _log_pretty_xml(response.text, 'response')

            NetConnect.failed_auth_attempts = 0

        elif re.search('^<(!DOCTYPE )?html', response.text, re.IGNORECASE):

            # TODO using DEMO environment this is the only way to test for bad AUTH.
            if re.search('app\.logonUrl', response.text):
                NetConnect.failed_auth_attempts += 1
                raise exceptions.FailedAuthException()
            elif re.search('changepw', response.text):
                raise exceptions.PasswordExpiredException()

        return response.text


class Ecals():
    net_connect_url = None

    def __init__(self, ecals_url):
        self.ecals_url = ecals_url

    def get_net_connect_url(self):
        if not self.net_connect_url:
            self.net_connect_url = Ecals.TimedUrl(self._fetch_net_connect_url(), constants.URL_EXPIRATION_IN_SECONDS)
        elif self.net_connect_url.is_expired():
            logging.info("Existing Net Connect URL is expired")
            self.net_connect_url.reset(self._fetch_net_connect_url())

        return self.net_connect_url.url

    def _fetch_net_connect_url(self):
        logging.info("Fetching new Net Connect URL from ECALS.")
        response = session.get_session().get(self.ecals_url)
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

    class TimedUrl():
        def __init__(self, url, seconds_til_expired):
            self.url = url
            self.start_time = time.time()
            self.seconds_til_expired = seconds_til_expired

        def is_expired(self):
            return (time.time() - self.start_time) >= self.seconds_til_expired

        def reset(self, url=None):
            self.url = url or self.url
            self.start_time = time.time()


def _dict_to_xml(data_dict, root=None):
    return dicttoxml.dicttoxml(data_dict, attr_type=False, custom_root=root)


def _log_pretty_xml(xml, header=None):
    header = "\n======%s======\n" % header.upper() if header else "\n"
    logging.info("%s%s" % (header, parseString(xml).toprettyxml()))
