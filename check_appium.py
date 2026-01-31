import requests
try:
    print("Checking Appium status...")
    r = requests.get('http://127.0.0.1:4723/status')
    print("Status Code:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print("Error connecting to Appium:", e)
