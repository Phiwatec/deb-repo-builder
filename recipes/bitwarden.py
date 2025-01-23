import os
from dotenv import load_dotenv
import requests

import urllib.request
URL = "https://api.github.com/repos/bitwarden/clients/releases"
load_dotenv()

username = os.environ.get('GH_USER')
token = os.environ.get('GH_TOKEN')
auth = (username, token)


def check_version(current_version,force):
    resp = requests.get(URL, auth=auth)
    data = resp.json()
    for release in data:
        if 'desktop' in release['tag_name']:
            new_version = release['tag_name']
            asset_url = release['assets_url']
            break

    print("Current version: " + current_version)
    print("Latest version: " + new_version)
    if new_version == current_version and not force:
        return (None, None)
    else:
        resp = requests.get(asset_url, auth=auth)
        asset_data = resp.json()

        for asset in asset_data:
            if '.deb' in asset['name']:
                return (new_version, (asset['browser_download_url'], asset['name']))
        return (None, None)


def build_package(version, location, data):
    # return

    urllib.request.urlretrieve(data[0], location+"/"+data[1])


if __name__ == "__main__":
    check_version('')
    build_package('', '')
