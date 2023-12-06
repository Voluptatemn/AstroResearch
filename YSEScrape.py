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

first_encounter = True
while response['previous'] != None:

    results = response['results']
    supernovea_created_date = int(results[-1]['created_date'][:10].replace('-', ''))
    if supernovea_created_date >= date_int:
        for i in range (len(results)):
            
            result = results[i]
            print(result['name'])
            try:
                redshift = result['redshift']
                if redshift == None:
                    host = session.get(result['host']).json()
                    redshift = host['redshift']
                    if redshift > max_redshift:
                        continue
                else:
                    if redshift > max_redshift:
                        continue
                dec = result['dec']
                if dec < min_declination:
                    continue
                magnitude = result['non_detect_limit']
                if magnitude < magnitude_min or magnitude > magnitude_max:
                    continue
                supernova_discovery_date = int(result['disc_date'][:10].replace('-', ''))
                if supernovea_created_date < date_int:
                    continue
                supernova_dict = {
                    'name': result['name'],
                    'ra': result['ra'],
                    'dec': dec,
                    'magnitude': magnitude,
                    'redshift': redshift,
                    'disc_date': result['disc_date']
                }
                potential_supernova.append(supernova_dict)
            except TypeError:
                continue
            except requests.exceptions.MissingSchema:
                continue
    else:
        if first_encounter:
            response = session.get(response['previous']).json()
            first_encounter = False
        else:
            break
   
    response = session.get(response['previous']).json()

session.close()

print(potential_supernova)












