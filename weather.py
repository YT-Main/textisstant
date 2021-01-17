import requests, json, time

class Weather:
    def __init__(self):
        # Parameters
        self.api_key = "94083afa77e93a2b611e6e446172f536"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city_name = "Toronto"
        self.complete_url = self.base_url + "appid=" + self.api_key + "&q=" + self.city_name + "&units=metric"

        # Get Data
        self.response = requests.get(self.complete_url)
        self.data = self.response.json()

    def weatherGet(self):
    # Print Results
        if self.data["cod"] != "404":
            self.main_data = self.data["main"]
            self.weather_data = self.data["weather"]
            self.temperature = self.main_data["temp"]

            return int(self.temperature)

        else:
            return(" City Not Found ")

# Created By: Yash Trivedi