import requests
import datetime as DT

# limit parameters for supernovea
max_redshift = 0.015 # <=

magnitude_max = 19

magnitude_min = 12

min_declination = -10 # >=

recent_discovery = 7 # days max
today = DT.date.today() - DT.timedelta(days=recent_discovery)
date_string = today.strftime("%Y%m%d")
date_int = int(date_string)
print(date_int)

follow_up_request = True # prioritize follow up requested 

potential_supernova = []

username = "hstacey"
password = "CDK700@Thacher"

payload = {
    'username': username,
    'password': password
}

api = 'https://ziggy.ucolick.org/yse/api/transients/?offset=148100'

session = requests.Session()
session.auth = (username, password)

response = session.get(api).json()
while response['previous'] != None:
    
    results = response['results']
    supernovea_date = int(results[0]['disc_date'][:10].replace('-', ''))
    if supernovea_date >= date_int:
        for i in range (len(results)):
                
            result = results[i]
                
            try:
                if result['redshift'] >= max_redshift:
                    continue
                if result['dec'] <= min_declination:
                    continue
            except TypeError:
                continue
    else:
        response = session.get(response['previous']).json()
   
    response = session.get(response['previous']).json()

session.close()













