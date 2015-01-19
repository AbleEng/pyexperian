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
    }
    
    ecals = services.Ecals('ECALS_URL')
    
    bpp = services.BusinessPremierProfile(config, ecals)
    
    result = bpp.query(business={'name': 'Franklin Barbecue', 'address': {'street': '900 E 11th St', 'city': 'Austin', 'state': 'TX', 'zip': '78702'}})
    
    print(result)
    
    
#### Raw XML query
If you don't want to use the simplified query parameters, you can pass in a pure XML string of the entire NetConnectRequest object.

    raw = services.Raw(config, ecals)
    
    result = raw.query("""
        <?xml version="1.0" encoding="UTF-8"?>
        <NetConnectRequest>
        ...
        </NetConnectRequest>
    """)
    
    print(result)

## Services

#### Business Premier Profile

    bpp = services.BusinessPremierProfile(config, ecals)
    result = bpp.query(business={..., address={...}})

#### SBCS

    sbcs = services.SBCS(config, ecals)
    result = sbcs.query(business={..., address={...}})
    
#### Business Owner Profile

    bop = services.BusinessOwnerProfile(config, ecals)
    result = bop.query(business={..., address={...}}, owner={..., address={}})
    

## Attributes

    TODO

## Debug 

    from pyexperian import services
    
    services.enable_debug()
   
## Tests

    nosetests
    
## Parsers

**This is where most help is needed**

There are basic parsers for each product to help spit out simple answers.

    from pyexperian import services, parsers    
    
    ...
    
    bop = services.BusinessPremierProfile(config, ecals)
    result = bpp.query(business={..., address={...}})
    
    parsed_result = parsers.BusinessPremierProfile(result)
   
    # Whether response shows a business match
    print(parsed_result.business_found())
   
    # Whether list of similars were returned.
    if parsed_result.has_list():
        similars = parsed_result.get_list()
        
        # Re-query using one of the similars
        business = {'experian_bin': similars[0]['experian_bin']}
        
        result = bpp.query(business=business)
