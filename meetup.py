import requests
from requests.auth import HTTPProxyAuth
import json
import os, os.path
import logging
from logging import NullHandler
from logging.config import fileConfig

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

class MeetupImages(object):
    """Meetup Class to download images from a Meetup group"""

    def __init__(self, api_key):
        self.api_key = api_key
        return None
    
    def downloadphoto(self, members):
        name = members['name']
        with open(f'./MeetupImages/{name}.jpeg', 'wb') as imagefile:
            imagefile.write(requests.request("GET", url=members['photo']['photo_link']).content)

    def getmembers(self, group_url, offset = 0):
        key = self.api_key
        requesturl = f'https://api.meetup.com/2/members?group_urlname={group_url}&key={key}&offset={offset}&order=name'
        headers = {
            'content-type': 'application/json;charset=utf-8',
            }
        response = requests.request("GET", url=requesturl, headers=headers)
        return json.loads(response.content)
    
    def getmemberphotos(self, members):
        [self.downloadphoto(member) for member in filter(lambda member: 'photo' in member.keys(), members)]