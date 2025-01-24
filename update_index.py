import requests

def notify_index_now():
    url = "https://www.bing.com/indexnow"
    params = {
        "url": "https://live.zbds.top",
        "key": "4c761c7c12a64659b9529b778f6a3b75"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Successfully notified IndexNow")
    else:
        print(f"Failed to notify IndexNow: {response.status_code}")

if __name__ == "__main__":
    notify_index_now() 