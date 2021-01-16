from flask import Flask, request, jsonify
from pprint import pprint
from weather import *
import time
import vonage

app = Flask(__name__)

client = vonage.Client(key='f3798314', secret='TXZnOvVkWorN2Qnt')


@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        pprint(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        pprint(data)

        recipient_number = data['msisdn']
        text = data['text']

        controller(recipient_number)


    return ('', 204)

def controller(recipient_number):
  check_weather(recipient_number)

def check_weather(recipient_number):
  old_val = 0
  while(True):
    temp_val = weatherGet()
    if(temp_val != old_val):
        send(recipient_number, weather_update())
        old_val = temp_val
    time.sleep(5)

def send(recipient_number, text):
    result = client.send_message({
        'from': '12013012405',
        'to': recipient_number,
    'text': '{}'.format(text),
    })

app.run(port=3000)


'''
Notes in code:
{'api-key': 'f3798314',
 'keyword': 'QWER',
 'message-timestamp': '2021-01-14 08:16:04',
 'messageId': '170000029E6BBBFE',
 'msisdn': '821074354789',
 'text': 'Qwer',
 'to': '12013012405',
 'type': 'text'
 'secret': 'TXZnOvVkWorN2Qnt'}

'''
