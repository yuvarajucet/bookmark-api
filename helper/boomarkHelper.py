import uuid
import base64
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse

def generateCategoryId():
    return str(uuid.uuid4())

def generateBookmarId():
    return str(uuid.uuid4())

def downloadWebsiteFavIcon(url):
    # remove unwanted warning message
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    favIconPath = '/favicon.ico'
    domain = urlparse(url).netloc
    image = requests.get('https://'+domain+favIconPath,verify=False).content
    baseValue = base64.b64encode(image)
    return baseValue