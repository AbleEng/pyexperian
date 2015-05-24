from pyexperian import services


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

    xml_out = services.dict_to_xml(d, root='NetConnectRequest')

    assert xml_out == _uglify_xml("""
<?xml version="1.0" encoding="UTF-8" ?>
<NetConnectRequest>
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

