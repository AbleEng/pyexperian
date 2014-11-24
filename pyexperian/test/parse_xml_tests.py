import xmltodict
from pyexperian import services, constants, parsers

xml_data = """
<CATALOG>
    <CD>
        <TITLE>Empire Burlesque</TITLE>
        <ARTIST>Bob Dylan</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>Columbia</COMPANY>
        <PRICE>10.90</PRICE>
        <YEAR>1985</YEAR>
    </CD>
    <CD>
        <TITLE>Hide your heart</TITLE>
        <ARTIST>Bonnie Tyler</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>CBS Records</COMPANY>
        <PRICE>9.90</PRICE>
        <YEAR>1988</YEAR>
    </CD>
    <CD>
        <TITLE>Greatest Hits</TITLE>
        <ARTIST>Dolly Parton</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>RCA</COMPANY>
        <PRICE>9.90</PRICE>
        <YEAR>1982</YEAR>
    </CD>
    <CD>
        <TITLE>Still got the blues</TITLE>
        <ARTIST>Gary Moore</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>Virgin records</COMPANY>
        <PRICE>10.20</PRICE>
        <YEAR>1990</YEAR>
    </CD>
</CATALOG>
"""


def test_xmltodict_parsing():
    data = xmltodict.parse(xml_data)

    assert data['CATALOG']['CD'][0]['PRICE'] == '10.90'

    cds = data['CATALOG']['CD']

    assert len(cds) == 4
    assert cds[3]['YEAR'] == '1990'


def test_get_val_helper():
    data = xmltodict.parse(xml_data)

    assert data['CATALOG']['CD'][0]['PRICE'] == parsers.BaseParser._get_dict_value(data, ['CATALOG', 'CD', 0, 'PRICE'])

    assert parsers.BaseParser._get_dict_value(data, ['CATALOG', 'CARLOS']) is None


def test_parse_error_code():
    data = xmltodict.parse("""<?xml version="1.0" standalone="no"?><NetConnectResponse xmlns="http://www.experian.com/NetConnectResponse"><CompletionCode>0000</CompletionCode><ReferenceId>StandAlone BOP</ReferenceId><TransactionId>14996435</TransactionId><Products xmlns="http://www.experian.com/ARFResponse"><BusinessProfile><ProcessingMessage><ProcessingAction code="031">BUSINESS OWNER/SMALL BUSINESS INTELLISCORE TERMS MESSAGE</ProcessingAction></ProcessingMessage></BusinessProfile></Products></NetConnectResponse>""")

    assert parsers.BaseParser._get_dict_value(data, ['NetConnectResponse', 'Products', 'BusinessProfile', 'ProcessingMessage', 'ProcessingAction', '@code']) == constants.TERMS_RESPONSE_CODE