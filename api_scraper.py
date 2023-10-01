import requests
import json

def fetch_all_police_events():
    url = "https://polisen.se/api/events"
    response = requests.get(url)
    if response.status_code == 200:
        with open('all_police_events.json', 'w', encoding='utf-8') as f:
            f.write(response.text)
        return json.loads(response.text)
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        return None

# Test function
all_events = fetch_all_police_events()
if all_events:
    print(f"Total number of events: {len(all_events)}")
