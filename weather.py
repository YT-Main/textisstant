import requests, json

# Parameters
api_key = "94083afa77e93a2b611e6e446172f536"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Toronto"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

# Get Data
response = requests.get(complete_url)
data = response.json()

def weatherGet():
# Print Results
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"]
        temperature = main_data["temp"]

        return int(temperature)

    else:
        return(" City Not Found ")


def weather_update():
    return 'Heads up! The temperature in your area has changed to:' + str(weatherGet()) +  "celcius"