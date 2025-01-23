import requests
from bs4 import BeautifulSoup
import subprocess
import os
URL = "https://developer.android.com/studio#downloads"
DL_URL = "https://redirector.gvt1.com/edgedl/android/studio/install/{version}/{file}"


def check_version(current_version,force):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.select(
        'button[data-modal-dialog-id="studio_chrome_os_bundle_download"]')
    for item in results:
        for content in item.contents:
            file = content
            break
        break

    version = file.split('-')[2]
    if version == current_version and not force:
        return (None, None)
    else:
        return (version, file)


def build_package(version, location, data):
    link = DL_URL.format(version=version, file=data)
    print(link)
    bashCommand = "sh ./recipes/android-studio/build.sh " + \
        link + " " + version + " "+location+" >/tmp/deblog"

    #process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,shell=True)
    os.system(bashCommand)
    print("Ran Bash Script")
