### Usage

    from pyexperian import pyexperian
    
    config = {
        'user_id': 'USER_ID', 
        'user_pw':'USER_PW', 
        'eai': 'EAI', 
        'vendor_number': 'VENDOR_NUMBER', 
        'sub_code': 'SUB_CODE', 
        'db_host': 'DB_HOST', 
        'ecals_url': 'ECALS_URL'
    }; 
    
    bpp = pyexperian.BusinessPremierProfile(config);
    
    resp = bpp.query(business={'name': 'Franklin Barbecue', 'address': {'street': '900 E 11th St', 'city': 'Austin', 'state': 'TX', 'zip': '78702'}})
    
    # Print the XML Response
    print(resp.text)