## Installation

    pip install pyexperian

## Usage

    from pyexperian import services
    
    config = {
        'user_id': 'USER_ID', 
        'user_pw':'USER_PW', 
        'eai': 'EAI', 
        'vendor_number': 'VENDOR_NUMBER', 
        'sub_code': 'SUB_CODE', 
        'db_host': 'DB_HOST'
    };
    
    ecals = services.Ecals('ECALS_URL')
    
    bpp = services.BusinessPremierProfile(config, ecals)
    
    resp_dict, resp_blob = bpp.query(business={'name': 'Franklin Barbecue', 'address': {'street': '900 E 11th St', 'city': 'Austin', 'state': 'TX', 'zip': '78702'}})
    
    print(resp_blob)
    
    
### Raw XML query
If you don't want to use the simplified query parameters, you can pass in a pure XML string of the entire NetConnectRequest object.

    bp = services.BaseProduct(config, ecals)
    resp_dict, resp_blob = bp.raw_query("""
        <?xml version="1.0" encoding="UTF-8"?>
        <NetConnectRequest>
        ...
        </NetConnectRequest>
    """)
    
    print(resp_blob)

## Services

#### Business Premier Profile

    bpp = services.BusinessPremierProfile(config, ecals)
    resp = bpp.query(business={..., address={...}})

#### SBCS

    sbcs = services.SBCS(config, ecals)
    resp = sbcs.query(business={..., address={...}})
    
#### Business Owner Profile

    bop = services.BusinessOwnerProfile(config, ecals)
    resp = bop.query(business={..., address={...}}, owner={..., address={}})
    

## Attributes

    TODO

## Debug 

    from pyexperian import services
    
    services.enable_debug()
    