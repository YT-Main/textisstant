import requests, json

class Covid:
    def __init__(self):
        self.url = "https://api.apify.com/v2/key-value-stores/fabbocwKrtxSDf96h/records/LATEST?"
        self.response = requests.get(self.url)
        self.data = self.response.json()
        self.Ontario = self.data["infectedByRegion"][6]

    def covidGet(self):
        return [self.Ontario["infectedCount"], self.Ontario["deceasedCount"]]
