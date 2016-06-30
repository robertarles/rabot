#!/usr/local/bin/python3
import requests
import json
from datetime import datetime as dt
from curator import Curator
from flask import Flask
from datetime import datetime, timedelta


class RaWeather():
    """
    Check tomorrows weather for conditions I want to be alerted on
    """
    # TODO: add use of alerting from config (ignoring schedule, e.g. 'oh shit, it's about to rain')
    def __init__(self, day=1):
        self.config = None
        self.activity = None
        self.forecastday = day  # 0 = today, 1 = tomorrow
        self.alertresponse = dict()
        self.notifications = list()
        self.weatherweathericonurl = None
        self.notificationposted = False
        self.lastnotificationpayload = None

        self.last_vault_weather_notification = {}

        self.author_name = 'rabot32-RaWeather'

        self.jobresults = list()

        self.curator = Curator()
        # run initializations below
        self.loadactivity()
        self.loadconfig()

    def loadconfig(self):
        try:
            with open('./raweather.conf', 'r') as json_data:
                self.config = json.load(json_data)
                json_data.close()
                # print('Starting Config: {}'.format(self.config))
        except FileNotFoundError:
            errormessage = "[ERROR] Config file not found [{}]".format(self.configfile)
            self.setnotification(errormessage)
            self.sendnotifications()
            print(errormessage)
            print(type(self.config))
            exit()
        except json.decoder.JSONDecodeError as jde:
            errormessage = "[ERROR] Error decoding JSON config file"
            self.setnotification(errormessage)
            self.sendnotifications()
            print(errormessage)
            print(type(self.config))
            print(jde)
            exit()

    def loadactivity(self):
        activity_docs = self.curator.get_recent_vault_activity(limit=1, author=self.author_name)
        if len(activity_docs) > 0:
            self.last_vault_weather_notification = activity_docs[0]
            print("[INFO] latest weather activity: {}".format(
                self.last_vault_weather_notification['date']))
        else:
            print("[INFO] no weather activity yet recorded")

    def getweather(self):
        response = requests.get(self.config['wundergroundurl']).json()
        self.alertresponse = requests.get(self.config['wundergroundalerturl']).json()
        # print(response)
        # print(self.alertresponse)
        return response['forecast']['simpleforecast']['forecastday'][self.forecastday]

    def checkweatherconditions(self, weather):
        forecasthigh = int(weather["high"]['fahrenheit'])
        forecastlow = int(weather['low']['fahrenheit'])
        self.weathericonurl = weather['icon_url']
        forecastconditions = weather['conditions']
        for notificationcondition in self.config['notificationconditions']:
            if notificationcondition in forecastconditions.lower():
                self.setnotification('{} tomorrow'.format(notificationcondition))
        if forecastlow <= self.config['notify']['temp']['min']:
            self.setnotification('Low tomorrow of {}'.format(forecastlow))
        if forecasthigh >= self.config['notify']['temp']['max']:
            self.setnotification('High tomorrow of {}'.format(forecasthigh))
        if self.alertresponse['alerts'] is not None:
            for alert in self.alertresponse['alerts']:
                self.setnotification('Weather ALERT: {}'.format(alert), type='alert')
        self.jobresults.append('Notifications to be sent: {}'.format(len(self.notifications)))

    def setnotification(self, subject, type='notification'):
        self.notifications.append({
            'message': subject,
            'type': type
        })

    def sendnotifications(self):
        curator = Curator()
        last_notification = None
        if len(self.last_vault_weather_notification) > 0:
            print("[DEBUG] sendnotifications last notification was at{}".format(
                self.last_vault_weather_notification['date']))
            last_notification = self.last_vault_weather_notification['date']
        else:
            print("[DEBUG] no previous weather notifications")
            last_notification = datetime.now() - timedelta(days=1)

        notification_at_entries = self.config['notify']['daily']

        for notify_at_entry in notification_at_entries:
            # get notify time with todays date as a datetime object
            # print("DEBUG {}".format(notify_at_entry))
            notify_at = dt.strptime(
                str(dt.now().date()) + ' ' + notify_at_entry, '%Y-%m-%d %H:%M'
            )
            # is the configured notification time past, and has no notification already been sent?
            print('[DEBUG] last notification {}'.format(last_notification))
            print('[DEBUG] notify at date time is {}'.format(notify_at))
            if (dt.now() >= notify_at) and (last_notification < notify_at):
                for notification in self.notifications:
                    if notification['type'] == 'notification':
                        message = '{}'.format(notification['message'])
                        curator.process(
                            message,
                            ["`message`", "`store`"],
                            author=self.author_name
                        )
                        self.lastnotificationpayload = message
                        self.jobresults.append("Attempted to send notification: {}".format(message))
                        self.notificationposted = True  # we've sent a notification (not an alert)
                    if notification['type'] == 'alert':
                        message_string = notification['message'].replace(
                            "Weather ALERT: ", '').replace(
                            "'", '"'
                            )
                        message_json = json.loads(message_string)
                        curator.process(
                            message_json['message'],
                            ["`message`", "`store`"],
                            author=self.author_name
                        )

    def check(self):
        weather = self.getweather()
        self.checkweatherconditions(weather)
        self.sendnotifications()
        return self.jobresults


if __name__ == '__main__':
    app = Flask(__name__)
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('{}.log'.format(__name__), maxBytes=10000, backupCount=5)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    raw = RaWeather()
    raw.check()
