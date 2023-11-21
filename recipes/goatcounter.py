import os
from dotenv import load_dotenv
import requests
import urllib.request
ARCH=['amd64','arm64']
URL = "https://api.github.com/repos/arp242/goatcounter/releases/latest"

load_dotenv()

username = os.environ.get('GH_USER')
token = os.environ.get('GH_TOKEN')
auth = (username, token)

def check_version(current_version):
    resp = requests.get(URL, auth=auth)
    data = resp.json()
    new_version = data['tag_name'][1:]
    print("Current version: " + current_version)
    print("Latest version: " + new_version)
    returndata = []
    if new_version == current_version:
        return (None, None)
    else:
        for arch in ARCH:
            for asset in data['assets']:
                #print(asset['name'])
                #print(f'goatcounter-{new_version}-linux-{arch}.gz')
                if asset['name'] == f'goatcounter-v{new_version}-linux-{arch}.gz':

                    returndata.append(
                        (asset['browser_download_url'], asset['name'], arch))

        if len(returndata) == 0:
            print("Error! New version but no matching assets found")
            return (None, None)

        else:
            return (new_version, returndata)




def build_package(version, location, data):
    for arch in data:
        link = arch[0]
        name = arch[1]
        arch_s = arch[2]
        bashCommand = f"sh ./recipes/goatcounter/build.sh {link} {version} {arch_s} {location}goatcounter_{version}_{arch_s}.deb" 
        os.system(bashCommand)
        print("Ran Bash Script")
