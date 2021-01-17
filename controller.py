from flask import Flask, request, jsonify
from pprint import pprint
from weather import Weather
from covid import Covid
from stocks import Stocks
from government import Government
from search import Search
from news import News
from chatbot import witBot
import threading
import time
import vonage

app = Flask(__name__)

client = vonage.Client(key='0c4254c4', secret='i7EFdIuz8Zpe4qer')

weather_instance = Weather()
covid_instance = Covid()
stock_instance = Stocks()
government_instance = Government()
search_instance = Search()
news_instance = News()
bot_instnace = witBot()

recipient_number = '14164009651'
name = "Yash"

@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        pprint(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        pprint(data)

        recipient_number = data['msisdn']
        text = data['text']

        controller(text)


    return ('', 204)

def controller(text):
    understood = bot_instnace.understand(text)
    print(understood)

    if(understood[0] == 'NULL'):
        if(text.lower() == 'hey'):
            send(recipient_number,"Hey, I'm Sophia your new personal assistant. You can text me any time night or day if you need any assistance.")
            time.sleep(2)
            send(recipient_number,"Silly me I'm on a new phone oculd you text me your name please?")
        
        if('yash' in text.lower()):
            send(recipient_number, "Hello Yash, I am all set up for you :) You can always ask me for help on how to use me just type in 'help'")
            time.sleep(2)
            send(recipient_number, "oh yeah. I almost forgot, here are the start up stats you wanted:")
            time.sleep(2)
            initialize(recipient_number)

    if(understood[0] == 'Weather'):
        send(recipient_number, ('Hey Yash, its ' + str(weather_instance.weatherGet()) + ' degrees. ' + temp_message(int(weather_instance.weatherGet()))))

    if(understood[0] == 'Stocks'):
        if(understood[1]['Ticker'].lower() == 'watchlist'):
            send(recipient_number, 'let me take a look')
            send(recipient_number, 'here is how your watchist is doing \n USD to PHP is' + str(stock_instance.get_data('USD_PHP')) + '\n KRW to USD is' + str(stock_instance.get_data('KRW_USD')) + '\n JPY to USD is' + str(stock_instance.get_data('JPY_USD')))
        else:
            send(recipient_number, 'Alright, so I have looked it up and the value of USD to PHP is ' + str(stock_instance.get_data(understood[1]['Ticker'])))

    if(understood[0] == 'thanks'):
        send(recipient_number, 'Any Time :)')

    if(understood[0] == 'government'):
        send(recipient_number, 'Sure let me see')
        send(recipient_number, is_government_update())

    if(understood[0] == 'search'):
        send(recipient_number, 'let me look it up')
        time.sleep(3)
        send(recipient_number, search_instance.search_info(text))

    if(understood[0] == 'news'):
        send(recipient_number, 'Here you go\nNEWS UPDATE: ' + news_update())

# Stocks
def load_stock(recipient_number):
    old_porfolio = [['USD_PHP', 0],['KRW_USD', 0],['JPY_USD', 0]]
    while(True):
        old_porfolio = check_stock(old_porfolio)
        time.sleep(3600)

def check_stock(old_porfolio):
    n = 0
    change = 0
    for i in old_porfolio:
        temp_price = stock_instance.get_data(i[0])
        if(i[1] != 0):
            change = (temp_price-i[1])/i[1]
        if((abs(change) > 0.00005) or (i[1] == 0)):
            send(recipient_number, 'Hey you might want to check on your posiiton in ' + i[0] + ', the value just shifted to ' + str(temp_price))
            time.sleep(1)
            i[1] = temp_price
        n+=1
    
    return old_porfolio
# Covid
def load_covid(recipient_number):
    old_covid = [0,0]
    while(True):
        old_covid = check_covid(recipient_number, old_covid)
        time.sleep(600)

def check_covid(recipient_number, old_covid):
    temp_val = covid_instance.covidGet()
    temp_infect = int(temp_val[0]) - int(old_covid[0])
    if(abs(temp_infect)> 10):
        send(recipient_number, 'There are ' + str(temp_val[0]) + ' people infected with COVID-19 in Ontario')
        time.sleep(1)

    temp_dead = int(temp_val[1]) - int(old_covid[1])
    if(abs(temp_dead) > 1):
        send(recipient_number, 'Sadly ' + str(temp_val[1]) + ' people have died Ontario from COVID')
        time.sleep(1)
    
    send(recipient_number, "it's pretty bad out there! Be Careful : )")
    time.sleep(1)
    return temp_val

# Weather
def temp_message(temp):
    if(temp<5):
        return "It'll be cold so stay warm."
    if(temp>25):
        return "Oh its warm, have fun outside."
def load_weather(recipient_number):
    old_val = None
    while(True):
        old_val = check_weather(recipient_number, old_val)
        print('weather')
        time.sleep(60)

def check_weather(recipient_number, old_val):
    temp_val = weather_instance.weatherGet()
    if(old_val != temp_val):
        send(recipient_number, 'Heads up the temperature in Toronto is currently ' + str(temp_val) + 'degrees')
    return temp_val

# Government
def load_government(recipient_number):
    while(True):
        temp_update = government_instance.get_alert()
        if(temp_update != 'NULL'):
            send(recipient_number, 'Yash, here is a urgent government alert that just got sent out: ' + temp_update)
        time.sleep(600)

def is_government_update():
    temp_update = government_instance.get_alert()
    if(temp_update != 'NULL'):
        return 'There is : ' + temp_update
    return 'No there is not'

# News
def load_news(recipient_number):
    old_news = None
    while(True):
        old_news = check_news(recipient_number, old_news)
        print('weather')
        time.sleep(60)

def check_news(recipient_number, old_news):
    temp_news = str(weather_instance.weatherGet())
    if(old_news != temp_news):
        send(recipient_number, 'News Update: ' + str(news_instance.get_polished_articles()))
    return temp_news

def news_update():
    news = news_instance.get_polished_articles()
    news_text = news[0]['title']
    return news_text
# Send
def send(recipient_number, text):
    result = client.send_message({
        'from': '15877603813',
        'to': recipient_number,
    'text': '{}'.format(text),
    })


def initialize(recipient_number):
    weather_tread = threading.Thread(target=load_weather, args=(recipient_number, ))
    weather_tread.start()
    covid_tread = threading.Thread(target=load_covid, args=(recipient_number, ))
    covid_tread.start()
    stock_tread = threading.Thread(target=load_stock, args=(recipient_number, ))
    stock_tread.start()
    government_tread = threading.Thread(target=load_government, args=(recipient_number, ))
    government_tread.start()
    news_tread = threading.Thread(target=load_news, args=(recipient_number, ))
    news_tread.start()

app.run(port=3000)


'''
Notes in code:
{'api-key': '0c4254c4',
 'keyword': 'QWER',
 'message-timestamp': '2021-01-14 08:16:04',
 'messageId': '170000029E6BBBFE',
 'msisdn': '821074354789',
 'text': 'Qwer',
 'to': '12013012405',
 'type': 'text'
 'secret': 'i7EFdIuz8Zpe4qer'}

'''
