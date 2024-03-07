import requests
# Function to fetch data from API
def fetch_data(api_url):
    response = requests.get(api_url)
    data = response.json()
    return data
