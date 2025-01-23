import requests
from pprint import pprint

# Structure payload.
payload = {
   'source': 'universal',
   'url': 'https://en.wikipedia.org/wiki/Human'
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('rohangai77@gmail.com', 'vaYFLPVz9UZY8yt'), #Your credentials go here
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with results.
pprint(response.json())