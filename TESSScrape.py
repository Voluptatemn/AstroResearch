# from astroquery.mast import Observations
# observations = Observations.query_criteria(obs_collection='TESS', target_name='25132999')
# print(observations)
# https://astroquery.readthedocs.io/en/latest/mast/mast.html#getting-started 
# https://mast.stsci.edu/api/v0/pyex.html#tess_searches 
'''
Depth > 6ppt, ?   
9 < Vmag < 16, done 
Elevation > 30 degrees, done  
the transit needs to be 90-100% full, ?
priority >= 3. ?
https://mast.stsci.edu/api/v0/_t_i_cfields.html
'''

import sys
import json
from astropy.table import Table
import numpy as np
import requests
from urllib.parse import quote as urlencode

def mast_query(request):
    """Perform a MAST query.
 
        Parameters
        ----------
        request (dictionary): The MAST request json object
 
        Returns head,content where head is the response HTTP headers, and content is the returned data"""
 
    # Base API url
    request_url='https://mast.stsci.edu/api/v0/invoke'
 
    # Grab Python Version
    version = ".".join(map(str, sys.version_info[:3]))
 
    # Create Http Header Variables
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain",
               "User-agent":"python-requests/"+version}
 
    # Encoding the request as a json string
    req_string = json.dumps(request)
    req_string = urlencode(req_string)
    
    # Perform the HTTP request
    resp = requests.post(request_url, data="request="+req_string, headers=headers)
 
    # Pull out the headers and response content
    head = resp.headers
    content = resp.content.decode('utf-8')
 
    return head, content

def set_filters(parameters):
    return [{"paramName":p, "values":v} for p,v in parameters.items()]

def set_min_max(min, max):
    return [{'min': min, 'max': max}]

filter = {
    "dec" : set_min_max(30, 90),
    "Vmag": set_min_max(9, 16),
    # "priority": set_min_max(0.003, 1000),
                
}

def tic_advanced_search():
    filts = set_filters(filter)
 
    request = {"service":"Mast.Catalogs.Filtered.Tic",
               "format":"json",
               "params":{
                   "columns":"COUNT_BIG(*)",
                   "filters": filts
               }}
 
    headers, out_string = mast_query(request)
    out_data = json.loads(out_string)
 
    return out_data

def tic_advanced_search_rows():
    filts = set_filters(filter)
 
    request = {"service":"Mast.Catalogs.Filtered.Tic.Rows",
               "format":"json",
               "params":{
                   "columns":"*",
                   "filters": filts
               }}
 
    headers, out_string = mast_query(request)
    out_data = json.loads(out_string)
 
    return out_data

def ctl_advanced_search():
    filts = set_filters(filter)
 
    request = {"service":"Mast.Catalogs.Filtered.Ctl",
               "format":"json",
               "params":{
                   "columns": "COUNT_BIG(*)",
                   "filters":filts
               }}
 
    headers, out_string = mast_query(request)
    out_data = json.loads(out_string)
 
    return out_data

def ctl_advanced_search_rows():
    filts = set_filters(filter)
 
    request = {"service":"Mast.Catalogs.Filtered.Ctl.Rows",
               "format":"json",
               "params":{
                   "columns": "*",
                   "filters": filts
               }}
 
    headers, out_string = mast_query(request)
    out_data = json.loads(out_string)
 
    return out_data
