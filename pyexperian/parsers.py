import xmltodict
from pyexperian import constants, exceptions

class BaseParser():

    # Helper function to simplify looking for a value nested deeply within a dictionary
    @classmethod
    def _get_dict_value(cls, d, key_list):
        if type(d) not in [dict, list, xmltodict.OrderedDict]:
            return d

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

    def has_list(self):
        return 'ListOfSimilars' in self.dict[self.product_id]

    def business_found(self):
        profile_type_code = self._get_dict_value(self.dict, [self.product_id, 'BusinessNameAndAddress', 'ProfileType', '@code'])
        return not profile_type_code or profile_type_code.strip() != 'NO RECORD'

    def __init__(self, xml):
        self.xml = xml

        d = xmltodict.parse(xml)
        self.dict = d['NetConnectResponse']

        # Check for 'Bad Request' error
        error_message = self._get_dict_value(self.dict, ['ErrorMessage'])
        if error_message:
            error_tag = self._get_dict_value(self.dict, ['ErrorTag'])
            raise exceptions.BadRequestException('Message: %s, Tag: %s' % (error_message, error_tag))

        self.dict = self.dict['Products']


class BusinessOwnerProfile(BaseParser):
    product_id = constants.BUSINESS_OWNER_PROFILE_ID

    def __init__(self, xml):
        BaseParser.__init__(self, xml)

        if self._get_dict_value(self.dict, [self.product_id, 'ProcessingMessage', 'ProcessingAction', '@code']) == constants.TERMS_RESPONSE_CODE:
            raise exceptions.TermsException()

    def owner_found(self):
        return None is not self._get_dict_value(self.dict, ['CreditProfile', 'ProfileSummary'])

class BusinessPremierProfile(BaseParser):
    product_id = constants.BUSINESS_PREMIER_PROFILE_ID


class SBCS(BaseParser):
    product_id = constants.SBCS_ID

