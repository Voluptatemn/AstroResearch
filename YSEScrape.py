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

while response['next'] != None:
    response = session.get(response['next']).json()

while response['previous'] != None:
    
    results = response['results']
    supernovea_date = int(results[-1]['disc_date'][:10].replace('-', ''))
    if supernovea_date >= date_int:
        for i in range (len(results)):
            
            result = results[i]
            print(result['name'])
            try:
                if result['redshift'] == None:
                    host = session.get(result['host']).json()
                    if host['redshift'] >= max_redshift:
                        continue
                else:
                    if result['redshift'] >= max_redshift:
                        continue
                if result['dec'] <= min_declination:
                    continue
                magnitude = result['non_detect_limit']
                if magnitude < magnitude_min or magnitude > magnitude_max:
                    continue
                potential_supernova.append(result['name'])
            except TypeError:
                continue
            except requests.exceptions.MissingSchema:
                continue
    else:
        break
   
    response = session.get(response['previous']).json()

session.close()

print(potential_supernova)












