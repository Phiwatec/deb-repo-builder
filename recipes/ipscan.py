import os
from dotenv import load_dotenv
import requests
import urllib.request
ARCH=['amd64','all']
URL = "https://api.github.com/repos/angryip/ipscan/releases/latest"

load_dotenv()

username = os.environ.get('GH_USER')
token = os.environ.get('GH_TOKEN')
auth = (username, token)

def check_version(current_version,force):
    resp = requests.get(URL, auth=auth)
    data = resp.json()
    new_version = data['tag_name']
    print("Current version: " + current_version)
    print("Latest version: " + new_version)
    returndata = []
    if new_version == current_version and not force:
        return (None, None)
    else:
        for arch in ARCH:
            for asset in data['assets']:
                if asset['name'] == f'ipscan_{new_version}_{arch}.deb':

                    returndata.append(
                        (asset['browser_download_url'], f'ipscan_{new_version}_{arch}.deb', arch))

        if len(returndata) == 0:
            print("Error! New version but no matching assets found")
            return (None, None)

        else:
            return (new_version, returndata)




def build_package(version, location, data):
    for arch in data:
        print(arch[0])
        urllib.request.urlretrieve(arch[0], location+"/"+arch[1])
