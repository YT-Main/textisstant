from wit import Wit

class witBot():

    def __init__(self):
        self.client = Wit("HSUCIEGVYHDMFUBRMJITK7KJUFB7SQHE")

    def understand(self, user_input):
        analysis = self.client.message(user_input)
        intent_data = analysis['intents']
        try:
            intent_data = intent_data[0]['name']
        except:
            intent_data = "NULL"

        entity_data = {}
        for k, v in analysis['entities'].items():
            entity_data.update({v[0]['name']: v[0]['value']})
        return [intent_data, entity_data]

# Written by: Chris Chambers