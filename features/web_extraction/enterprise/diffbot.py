from client import DiffbotClient,DiffbotCrawl
from config import API_TOKEN
import pprint
import time

def diffbot_extract(url):
    diffbot = DiffbotClient()
    token = "da81fb64fb93302abac71ecbbdd0745a"
    api = "article"
    response = diffbot.request(url, token, api)
    print("\nPrinting response:\n")
    pp = pprint.PrettyPrinter(indent=4)
    response_data = pp.pformat(response)
    return response_data