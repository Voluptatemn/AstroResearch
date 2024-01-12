import requests
import datetime as DT
import time 
import os

class YSE_worm:
    
    def __init__(self, max_redshift = 0.015, magnitude_max = 19, magnitude_min = 12, min_declination = -10, recent_discovery = 7, follow_up_request = True, username = "hstacey", password = "CDK700@Thacher", api = 'https://ziggy.ucolick.org/yse/api/transients/?offset=152400', log_file_path = '/Users/qiangangsamwang/Documents/GitHub/AstroResearch/log_file.log') -> None:
        
        self.max_redshift = max_redshift
        self.magnitude_max = magnitude_max
        self.magnitude_min = magnitude_min
        self.min_declination = min_declination
        self.recent_discovery = recent_discovery
        self.follow_up_request = follow_up_request
        self.username = username
        self.password = password
        self.api = api
        self.log_file_path = log_file_path
        
    def dates(self):
    
        today = DT.date.today() - DT.timedelta(days=self.recent_discovery)
        date_string = today.strftime("%Y%m%d")
        date_int = int(date_string)
        return date_int
    
    def scrape(self):
            
        potential_supernova = []

        session = requests.Session()
        session.auth = (self.username, self.password)

        response = session.get(self.api).json()
        # print("Connect successfully")
        
        new_api = self.api
        # goes to the back of the sequence if not in the back right now
        while response['next'] != None:
            new_api = response['next']
            response = session.get(response['next']).json()

        first_encounter = True
        while response['previous'] != None:
            
            # check the page if the entire page is already greater than mimunim allowed dates
            # use created dates because the page is ordered by created dates 
            results = response['results']
            supernovea_created_date = int(results[-1]['created_date'][:10].replace('-', ''))
            date_int = self.dates()
            if supernovea_created_date >= date_int:
                for i in range (len(results)):
                    
                    result = results[i]
                    # print(result['name'])
                    try:
                        # check redshift if greater than the maxmimum redshift
                        redshift = result['redshift']
                        if redshift == None:
                            host = session.get(result['host']).json()
                            redshift = host['redshift']
                            if redshift >= self.max_redshift:
                                continue
                        else:
                            if redshift >= self.max_redshift:
                                continue
                        
                        # check dec if less then minmum declination
                        dec = result['dec']
                        if dec < self.min_declination:
                            continue
                        
                        # check if magnitude if less then min or greater than max
                        magnitude = result['non_detect_limit']
                        if magnitude < self.magnitude_min or magnitude > self.magnitude_max:
                            continue
                        
                        # check if the discovery date is older then the allowed window
                        supernova_discovery_date = int(result['disc_date'][:10].replace('-', ''))
                        if supernovea_created_date < date_int:
                            continue
                        
                        # create the return dict
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
            # adding a potential fail safe for two consecutive older created dates garentees there is no more applicable supernova to search
            else:
                if first_encounter:
                    response = session.get(response['previous']).json()
                    first_encounter = False
                else:
                    break
            # move the session
            response = session.get(response['previous']).json()

        session.close()
         
        return potential_supernova, new_api
    
    def log(self):
        
        start_time = time.time()
        
        current_time = DT.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        potential_supernova, new_api = self.scrape()
        
        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        elapsed_minutes = int(elapsed_time_seconds // 60)
        elapsed_seconds = int(elapsed_time_seconds % 60)
        
        with open(self.log_file_path, 'a') as f:
            f.write(f"Current time: {formatted_time}\n")
            f.write(f"Potential_supernova: {potential_supernova}\n")
            f.write(f"new_api: {new_api}\n")
            f.write(f"Job time: {elapsed_minutes} minutes and {elapsed_seconds} seconds")
            
    def is_log_file_empty(self):
        return os.path.getsize(self.log_file_path) == 0
            
if __name__ == "__main__":
    
    worm = YSE_worm()
    
    if worm.is_log_file_empty():
        worm.log()
    else:
        # Open a file for reading
        with open('log_file.log', 'r') as file:
            # Read the entire content of the file
            for line in file:
                if line.startswith('new_api'):
                    new_api = line[9:]
                    worm.api = new_api
                    break
            worm.log()
            















