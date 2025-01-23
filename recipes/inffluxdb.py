import os
from dotenv import load_dotenv
import requests
import urllib.request
ARCH=['amd64','arm64']
URL = "https://api.github.com/repos/influxdata/influxdb/releases/latest"

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
    returndata = []
    if new_version == current_version and not force:
        return (None, None)
    else:
        for arch in ARCH:
            print(f'https://dl.influxdata.com/influxdb/releases/influxdb2_{new_version}-1_{arch}.deb')
            returndata.append((f'https://dl.influxdata.com/influxdb/releases/influxdb2_{new_version}-1_{arch}.deb', f'influxdb_{new_version}_{arch}.deb', arch))

        if len(returndata) == 0:
            print("Error! New version but no matching assets found")
            return (None, None)

        else:
            return (new_version, returndata)




def build_package(version, location, data):
    for arch in data:
        urllib.request.urlretrieve(arch[0], location+"/"+arch[1])
