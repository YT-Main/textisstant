import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
import phonenumbers
from phonenumbers import timezone

class Reminder:
    def __init__(self):
        self.user_reminder_data = {}

    def alert_recent_event(self, user_number, hours_threshold=None, minutes_threshold=60):
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
        now = datetime.now()

        time_within_alert = now + timedelta(minutes=minutes_threshold)
        df = df.loc[(now < df['dateTime'])&(df['dateTime']<= time_within_alert)]
        if not df.empty:
            values = df.values[:top_k]
            urgent_events = {}
            urgent_events['user_number'] = user_number
            urgent_events['event'] = values[0,0]
            urgent_events['dateTime'] = values[0,1]

            return events
        else:
            return None

    def get_user_events(self, user_number):
        return self.user_reminder_data[user_number]

    def add_user_event(self, user_number, event, minutes_later):
        dateTime = datetime.now() + timedelta(minutes=minutes_later)
        if user_number in self.user_reminder_data:
            self.user_reminder_data[user_number].append({'event':event, 'dateTime':dateTime})
        else:
            self.user_reminder_data[user_number] = [{'event':event, 'dateTime':dateTime}]

