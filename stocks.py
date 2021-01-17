import requests, json

class Stocks:
  def __init__(self):
    self.api_key = 'addf2eef6d5323147a35'

  def get_data(self, stock):
    self.stock = str(stock)
    self.url = 'https://free.currconv.com/api/v7/convert?q=' + self.stock + '&compact=ultra&apiKey=' + self.api_key

    # Data
    self.response = requests.get(self.url)
    self.data = self.response.json()
    self.info = self.data[self.stock]

    # Return Data
    return self.info

# Created By: Yash Trivedi