## Installation

    pip install pyexperian

## Usage

    from pyexperian import services
    
    net_connect = services.NetConnect({
        'user_id': 'USER_ID', 
        'user_pw':'USER_PW', 
        'eai': 'EAI', 
        'vendor_number': 'VENDOR_NUMBER', 
        'sub_code': 'SUB_CODE', 
        'db_host': 'DB_HOST',
        'ecals_url': 'ECALS_URL'
    })
   
	# SBCS
	response_xml = net_connect.query('SmallBusinessCreditShare', {
		'AddOns': {
			'SCORE': 'Y',
			'BP': 'Y'
		},
		'BusinessApplicant': {
			'BusinessName': 'Experian',
			'CurrentAddress': {
				'Street': '475 Anton Blvd',
				'City': 'Costa Mesa',
				'State': 'CA',
				'Zip': '92626'
			}
		}
	})


	# Business Premier Profile
	response_xml = net_connect.query('PremierProfile', {
		'BusinessApplicant': {
			'BusinessName': 'Experian',
			'CurrentAddress': {
				'Street': '475 Anton Blvd',
				'City': 'Costa Mesa',
				'State': 'CA',
				'Zip': '92626'
			}
		}
	})

	# Business Owner Profile
	response_xml = net_connect.query('BusinessProfile', {
		'Options': {
			'CustomerName': 'CustomerName'
		},
		'AddOns': {
			'StandAlone': 'Y'
		},
		'BusinessApplicant': {
			'BusinessName': 'Experian',
			'CurrentAddress': {
				'Street': '475 Anton Blvd',
				'City': 'Costa Mesa',
				'State': 'CA',
				'Zip': '92626'
			}
		},
		'BusinessOwner': {
			'SSN': '887487109',
			'OwnerName': {
				'First': 'Derrick',
				'Surname': 'Benson',
			},
			'CurrentAddress': {
				'Street': '7600 Trumbower Trl',
				'City': 'Millington',
				'State': 'MI',
				'Zip': '48746'
			}
		}
	})

