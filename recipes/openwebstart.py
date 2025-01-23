import os
from dotenv import load_dotenv
import requests

import urllib.request
URL = "https://api.github.com/repos/karakun/OpenWebStart/releases/latest"
load_dotenv()

username = os.environ.get('GH_USER')
token = os.environ.get('GH_TOKEN')
auth = (username, token)


def check_version(current_version,force):
    resp = requests.get(URL, auth=auth)
    data = resp.json()
    new_version = data['tag_name'][1:]
    print("Current version: " + current_version)
    print("Latest version: " + new_version)
    if new_version == current_version and not force:
        return (None, None)
    else:
        for asset in data['assets']:
            if asset['name'] == f'OpenWebStart_linux_{new_version.replace(".", "_")}.deb':
                return (new_version, (asset['browser_download_url'], f"openwebstart_{new_version}_all.deb"))
        return (None, None)


def build_package(version, location, data):
    urllib.request.urlretrieve(data[0], location+"/"+data[1])
