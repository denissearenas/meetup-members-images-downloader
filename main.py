import logging
from logging.config import fileConfig
from configparser import ConfigParser
import os, os.path

from meetup import MeetupImages
#import imageworker

# Create the Working folders
working_folders = ['logs','MeetupImages']
[os.makedirs(folder) for folder in working_folders if not os.path.exists(folder)]

# Load Configuration for reading parameters
Config = ConfigParser()
Config.read('settings.ini')

# Load log config
fileConfig('logging_config.ini')
logger = logging.getLogger()

def meetupworker(api_key, meetup_group):
    # meetup worker : Get the Meetup Members and then images
    meetup_worker = MeetupImages(api_key=api_key)
    download_finished = False
    offset = 0
    while not download_finished:
        members = meetup_worker.getmembers(meetup_group,offset)
        meetup_worker.getmemberphotos(members['results'])
        offset += 1
        if members['meta']['next'] == "":
            download_finished = True

if __name__ == "__main__":
    
    # Read Meetup API Key and group details
    api_key = Config.get('meetup', 'api_key')
    meetup_group = Config.get('meetup', 'meetup_group')

    meetupworker(api_key=api_key, meetup_group=meetup_group)
