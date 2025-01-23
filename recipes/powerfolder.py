import os
import requests
import urllib.request
from bs4 import BeautifulSoup,SoupStrainer
ARCH=['amd64','arm64']
URL = "https://my.powerfolder.com/download_client"


username = os.environ.get('GH_USER')
token = os.environ.get('GH_TOKEN')
auth = (username, token)

def check_version(current_version,force):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links=soup.find_all('a')
    for link in links:
        if link.contents[0]== '.deb (x86_64)':
                link=link['href']
                break
        
    version=link.split('/')[-1].split('_')[1]

    return (version if version != current_version and not force else None,link)

    

    





def build_package(version, location, data):
    urllib.request.urlretrieve(data, location+"/"+f'PowerFolder_{version}_amd64.deb')

if __name__=='__main__':
    check_version(None)
