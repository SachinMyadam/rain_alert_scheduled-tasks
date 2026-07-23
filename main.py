import os
import requests
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {
    'http': os.environ.get('http_proxy', 'http://proxy.server:3128'),
    'https': os.environ.get('https_proxy', 'http://proxy.server:3128')
}
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWN_API_KEY")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
weather_params = {
    "lat": 17.509489,
    "lon":78.304077,
    "appid":api_key,
    "cnt": 4,

}
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        to="+917095656881",
        from_="+12409237742",
        body="It's going to rain.Remember to bring an umbrella.")
    print(message.status)


