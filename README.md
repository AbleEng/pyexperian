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
    
    resp = bpp.query(business={'name': 'Franklin Barbecue', 'address': {'street': '900 E 11th St', 'city': 'Austin', 'state': 'TX', 'zip': '78702'}})
    
    print(resp.text)
    
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
    