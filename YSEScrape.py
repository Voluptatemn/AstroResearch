import requests

file = open("ysescrapingsetting.txt", "r+")
content = file.read()
page_starting = content

username = "hstacey"
password = "CDK700@Thacher"

payload = {
    'username': username,
    'password': password
}

api = 'https://ziggy.ucolick.org/yse/api/transients/'

if page_starting != '0':
    api = page_starting

session = requests.Session()
session.auth = (username, password)

response = session.get(api).json()
print(int(response['results'][0]['name'][:4]))

while response['next'] != None:
    
    if page_starting == '0':
        year = int(response['results'][0]['name'][:4])
        print(response['previous'])
        if year == 2023:
            file.truncate(0)
            file.write(response['previous'])
            file.close()
            break
    '''
    Do something
    '''
    response = session.get(response['next']).json()

session.close()













