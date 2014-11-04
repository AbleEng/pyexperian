from pyexperian.lib import dicttoxml


def _uglify_xml(xml_output):
    ugly = xml_output.replace("    ", "").replace("\n", "")
    return ugly


def test_xml_request_building():
    d = {
        'EAI': '11111111',
        'DBHost': 'BISPROD',
        'ReferenceId': 'user1abc001',
        'Request xmlns="http://www.experian.com/WebDelivery" version="1.0"': {
            'Products': {
                'PremierProfile': {
                    'Subscriber': {
                        'OpInitials': 'GG',
                        'SubCode': '0123456'
                    },
                    'OutputType': {
                        'XML': {
                            'Verbose': 'Y'
                        }
                    }
                }
            }
        }
    }

    xml_out = dicttoxml.dicttoxml(d, attr_type=False, custom_root='NetConnectRequest xmlns="http://www.experian.com/NetConnect" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.experian.com/NetConnect NetConnect.xsd"')

    assert xml_out == _uglify_xml("""
<?xml version="1.0" encoding="UTF-8" ?>
<NetConnectRequest xmlns="http://www.experian.com/NetConnect" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.experian.com/NetConnect NetConnect.xsd">
    <EAI>11111111</EAI>
    <DBHost>BISPROD</DBHost>
    <ReferenceId>user1abc001</ReferenceId>
    <Request xmlns="http://www.experian.com/WebDelivery" version="1.0">
        <Products>
            <PremierProfile>
                <Subscriber>
                    <SubCode>0123456</SubCode>
                    <OpInitials>GG</OpInitials>
                </Subscriber>
                <OutputType>
                    <XML>
                        <Verbose>Y</Verbose>
                    </XML>
                </OutputType>
            </PremierProfile>
        </Products>
    </Request>
</NetConnectRequest>""")

