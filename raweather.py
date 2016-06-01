#!/usr/local/bin/python3
import requests
import json
from datetime import datetime as dt
from ratwitter import RaTwitter
from flask import Flask


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

        self.loadactivity()
        self.loadconfig()

        self.jobresults = list()

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
        try:
            with open('raweather.activity', 'r') as json_data:
                self.activity = json.load(json_data)
                json_data.close()
                print('Starting Activity: {}'.format(self.activity))
        except FileNotFoundError:
            errormessage = "[ERROR] Activity file not found"
            self.setnotification(errormessage)
            self.sendnotifications()
            print(errormessage)
            print(type(self.activity))
        except json.decoder.JSONDecodeError as jde:
            errormessage = "[ERROR] Error decoding JSON activity file"
            self.setnotification(errormessage)
            self.sendnotifications()
            print(errormessage)
            print(type(self.activity))
            print(jde)
            exit(1)

    def saveactivity(self):
        try:
            with open('raweather.activity', 'w') as json_file:
                print('[DEBUG] writing {} to activity file'.format(self.activity))
                json_file.writelines(json.dumps(self.activity))
        except Exception as e:
            print(e)

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
        rat = RaTwitter()
        last_notification = dt.strptime(
            self.activity['lastdailynotification']['date'], "%Y-%m-%d %H:%M:%S.%f"
        )
        notification_at_entries = self.config['notify']['daily']

        for notify_at_entry in notification_at_entries:
            # get notify time with todays date as a datetime object
            # print("DEBUG {}".format(notify_at_entry))
            notify_at = dt.strptime(
                str(dt.now().date()) + ' ' + notify_at_entry, '%Y-%m-%d %H:%M'
            )
            # is the configured notification time past, and has no notification already been sent?
            # print('[DEBUG] last notification {}'.format(lastnotification))
            # print('[DEBUG] notify at date time is {}'.format(notify_at))
            if (dt.now() >= notify_at) and (last_notification < notify_at):
                for notification in self.notifications:
                    if notification['type'] == 'notification':
                        message = '{}'.format(notification['message'])
                        rat.direct_message(
                            "metabot32",
                            message
                        )
                        self.lastnotificationpayload = message
                        self.jobresults.append("Attempted to send notification: {}".format(message))
                        self.notificationposted = True  # we've sent a notification (not an alert)
                    if notification['type'] == 'alert':
                        # [2016-06-01 13:33:25.661834] switch to twitter dmgit s
                        rat.direct_message(
                            "metabot32",
                            notification['message']
                        )
                        # payload = r'{"text": "' + notification['message'] + r'"}'
                        # requests.post(self.config['slackposturl'], payload, '\n')

    def check(self):
        weather = self.getweather()
        self.checkweatherconditions(weather)
        self.sendnotifications()
        if self.notificationposted:
            self.activity['lastdailynotification']['message'] = self.lastnotificationpayload
            self.activity['lastdailynotification']['date'] = "{}".format(dt.now())
        print('Final activity: {}'.format(self.activity))
        self.saveactivity()
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
