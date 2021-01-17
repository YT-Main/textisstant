import requests,json

class Search:
  def search_info(self, query):
    # set up the request parameters
    self.params = {
      'api_key': '24AB0B54FC134D55AE4A5A2B9344F508',
      'q': query,
      'gl': 'us',
      'hl': 'en',
      'location': 'United States',
      'google_domain': 'google.com'
    }

    # make the http GET request to Scale SERP
    self.api_result = requests.get('https://api.scaleserp.com/search', self.params)
    self.data = self.api_result.json()
    self.info = self.data['knowledge_graph']['description']
    # print the JSON response from Scale SERP
    return self.info