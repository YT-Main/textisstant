import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
import phonenumbers
from phonenumbers import timezone

class Reminder:
    def __init__(self):
        self.utc=pytz.timezone('Canada/Pacific') #Work on timezone
        self.user_reminder_data = {}

    def alert_topk_recent_events(self, user_number, top_k=3, hours_threshold=None, minutes_threshold=60):
        '''
        OUTPUT: top_k events sorted in most urgent scheduling. 
        Events is dictionary containing
            summary: the name of event
            location: the name of location; if not specified, returns NaN
            start: the start of event; if not specified, returns date in 12 AM time
        Or None, if there are no urgent events to alert
        '''
        #Hours/minutes threshold: alert events that are only within how many hours/minutes before event start.
        if hours_threshold is not None:
            minutes_threshold += (hours_threshold * 60)

        events = self.get_user_events(user_number)

        #Convert dateTime string to datetime object
        #Localize into UTC timezone in order to normalize all dates into offset aware datetimes, not naive
        df = pd.DataFrame(events)
        df = df.sort_values(by='dateTime')
        print(df)
        now = self.utc.localize(datetime.now())

        time_within_alert = now + timedelta(minutes=minutes_threshold)
        df = df.loc[(now < df['dateTime'])&(df['dateTime']<= time_within_alert)]
        if not df.empty:
            values = df.values[:top_k]
            events = {}
            events['summary'] = values[:,0]
            events['location'] = values[:,1]
            events['start'] = values[:,2]

            return events
        else:
            return None

    def get_user_events(self, user_number):
        return self.user_reminder_data[user_number]

    def add_user_event(self, user_number, event, dateTime):
        dateTime = pd.to_datetime(dateTime)
        if user_number in self.user_reminder_data:
            self.user_reminder_data[user_number].append({'event':event, 'dateTime':dateTime})
        else:
            self.user_reminder_data[user_number] = [{'event':event, 'dateTime':dateTime}]

remind = Reminder()
remind.add_user_event('1234', 'asdf', '2021-01-19T18:00:00.000-08:00')
remind.alert_topk_recent_events('1234')
