#!./venv/bin/python
from flask import Flask, make_response, request
from os import getenv
from dotenv import load_dotenv
import requests


app = Flask(__name__)
load_dotenv()
GEO_API_KEY = getenv("GEO_API_KEY")
TEMP_API_KEY = getenv("TEMP_API_KEY")


@app.route("/")
def index_route():
    return "Hello World!"


@app.route("/api/hello", strict_slashes=False)
def hello_route():
    """Get the city of the user and the temperature of the city"""
    client_name = request.args.get("name", "Mentor 🙌")
    client_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

    response = {"client_ip": client_ip}
    city = get_ip_info(client_ip)
    if city:
        city = city.get("names", {}).get("en", "Unknown")
        response["city"] = city
    city_temp = get_city_temp(city)

    response["gretting"] = \
        f"Hello {client_name}!, the temperature is {city_temp} degrees in {city}"
    return make_response(response, 200)


def get_ip_info(ip):
    """Uses the ip of the remote user to get the city"""
    if GEO_API_KEY is None:
        return None
    url = f"https://api.geoapify.com/v1/ipinfo?{ip}&apiKey={GEO_API_KEY}"
    ip_info = requests.get(url).json()
    return ip_info


def get_city_temp(city):
    """Given a city get the temperature of the city"""
    url = \
        f"https://api.weatherapi.com/v1/current.json?key={TEMP_API_KEY}&q={city}&aqi=no"
    temp_info = requests.get(url).json()
    return temp_info.get("current", {}).get("temp_c", 0)


if __name__ == "__main__":
    app_port = int(getenv("APP_PORT", 5000))
    app_host = str(getenv("APP_HOST", "0.0.0.0"))
    app.run(host=app_host, port=app_port, debug=True)
