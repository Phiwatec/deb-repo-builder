from dotenv import load_dotenv
import requests
import os
import urllib.request
URL = "https://api.github.com/repos/czerwonk/ping_exporter/releases/latest"
load_dotenv()
ARCH = ['amd64', 'arm64']
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
                if asset['name'] == f'ping_exporter_{new_version}_linux_{arch}.deb':

                    returndata.append(
                        (asset['browser_download_url'], asset['name'], arch))

        if len(returndata) == 0:
            print("Error! New version but no matching assets found")
            return (None, None)

        else:
            return (new_version, returndata)


def build_package(version, location, data):

    # print(link)
    #    print(f'Location {location}')
    for arch in data:
        link = arch[0]
        bashCommand = f"sh ./recipes/prometheus-ping-exporter/build.sh {link} {version} {location}prometheus-ping-exporter_{version}_linux_{arch[2]}.deb {arch[2]} >/tmp/deblog"
        os.system(bashCommand)
        print("Ran Bash Script")
