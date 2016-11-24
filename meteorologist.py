#!/usr/local/bin/python3
import requests
import json
import os
from datetime import datetime as dt
from curator import Curator
from flask import Flask
from datetime import datetime, timedelta
from cartographer import Cartographer


class Meteorologist():
    """
    Check tomorrows weather for conditions I want to be alerted on
    """
    # TODO: add use of alerting from config (ignoring schedule, e.g. 'oh shit, it's about to rain')
    def __init__(self, day=1):
        self.config = None
        self.activity = None
        self.forecastday = day  # 0 = today, 1 = tomorrow
        self.alertresponse = {}
        self.notifications = []
        self.notificationposted = False
        self.lastnotificationpayload = None

        self.last_vault_weather_notification = {}

        self.DEFAULT_LOCATION = "34.1129745,-117.1628703"  # = "CA/Highland"
        self.iphone_ra_location_latest = self.get_device_location("iphone_ra")

        self.author_name = 'rabot32-Meteorologist'

        self.jobresults = []

        self.curator = Curator()
        # run initializations below
        self.loadactivity()
        self.loadconfig()

    def loadconfig(self):
        try:
            with open(os.path.expanduser('~') + '/.rabot/meteorologist.conf', 'r') as json_data:
                self.config = json.load(json_data)
                json_data.close()
                # print('[DEBUG] Starting Config: {}'.format(self.config))
        except (OSError, IOError):
            print("[EXCEPTION] self.config type is [{}]".format(type(self.config)))
            errormessage = "[EXCEPTiON] Config file not found [{}]".format(self.config)
            print("[EXCEPTION] {}".format(errormessage))
            self.setnotification(errormessage)
            self.sendnotifications()
            exit()
        except Exception as jde:
            errormessage = "[EXCEPTION] Error decoding JSON config file"
            print("[EXCEPTION] {}".format(errormessage))
            print(type(self.config))
            print("[EXCEPTION] {}".format(jde))
            self.setnotification(errormessage)
            self.sendnotifications()
            exit()

    def loadactivity(self):
        activity_docs = self.curator.get_recent_vault_activity(limit=1, author=self.author_name)
        if len(activity_docs) > 0:
            self.last_vault_weather_notification = activity_docs[0]
            print("[INFO] latest weather activity: {}".format(
                self.last_vault_weather_notification['date']))
        else:
            print("[INFO] no weather activity yet recorded")

    def get_device_location(self, device="iphone_ra"):
        location = self.DEFAULT_LOCATION
        try:
            with open(
                os.path.expanduser('~') + '/.rabot/' + device + "_location.json", "r"
            ) as device_location_file:
                device_location_json = json.loads(device_location_file.read())
                current_location = "{},{}".format(
                    device_location_json["latitude"],
                    device_location_json['longitude']
                )
                # only use this current location if its far from home (not on a drive or at work)
                home_lat = float(self.DEFAULT_LOCATION.split(",")[0])
                home_long = float(self.DEFAULT_LOCATION.split(",")[1])
                default_coords = {"lat": home_lat, "long": home_long}
                current_coords = {
                    "lat": device_location_json["latitude"],
                    "long": device_location_json['longitude']
                }
                cort = Cartographer()
                distance_from_home = cort.haversine(default_coords, current_coords)
                if distance_from_home["miles"] > 100:
                    location = current_location
        except FileNotFoundError as fnfe:
            print("[EXCEPTION] FILE: [{}]".format(os.path.expanduser('~') + '/.rabot/' + device + "_location.json", "r"))
            print("[EXCEPTION] Device Location File Not Found \n {}".format(fnfe))
        except Exception as e:
            print("[EXCEPTION] JSON decode exception caught?\n {}".format(e))
        return location

    def getweather(self):
        url = self.config['wundergroundurl'].replace("[LOCATION]", self.iphone_ra_location_latest)
        # print("[DEBUG] checking {}".format(url))
        response = requests.get(url).json()
        self.alertresponse = requests.get(self.config['wundergroundalerturl']).json()
        # print(response)
        # print(self.alertresponse)
        return response['forecast']['simpleforecast']['forecastday'][self.forecastday]

    def checkweatherconditions(self, weather):
        forecasthigh = int(weather["high"]['fahrenheit'])
        forecastlow = int(weather['low']['fahrenheit'])
        icon_name = weather['icon']
        forecastconditions = weather['conditions']
        # print("[DEBUG] forcastconditions [{}]".format(forecastconditions.lower()))
        for notificationcondition in self.config['notificationconditions']:
            # print('[DEBUG]{}, {} in {}'.format(
            #     notificationcondition.lower() in forecastconditions.lower(),
            #     notificationcondition.lower(), forecastconditions.lower()))
            if notificationcondition.lower() in forecastconditions.lower():
                self.setnotification(
                    '[{}] Notification of {} tomorrow'.format(icon_name, notificationcondition))
        if forecastlow <= self.config['notify']['temp']['min']:
            self.setnotification(
                '[{}] Low tomorrow of {}'.format(icon_name, forecastlow))
        if forecasthigh >= self.config['notify']['temp']['max']:
            self.setnotification(
                '[{}] High tomorrow of {}'.format(icon_name, forecasthigh))
        if 'alerts' in self.alertresponse.keys() and self.alertresponse['alerts'] is not None:
            for alert in self.alertresponse['alerts']:
                self.setnotification(
                    '[{}] Weather ALERT: {}'.format(icon_name, alert), type='alert')
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
            # print("[DEBUG] sendnotifications last notification was at{}".format(
            #     self.last_vault_weather_notification['date']))
            last_notification = self.last_vault_weather_notification['date']
        else:
            # print("[DEBUG] no previous weather notifications")
            last_notification = datetime.now() - timedelta(days=1)
        notification_at_entries = self.config['notify']['daily']

        for notify_at_entry in notification_at_entries:
            # get notify time with todays date as a datetime object
            # print("DEBUG {}".format(notify_at_entry))
            notify_at = dt.strptime(
                str(dt.now().date()) + ' ' + notify_at_entry, '%Y-%m-%d %H:%M'
            )
            # is the configured notification time past, and has no notification already been sent?
            # print('[DEBUG] last notification {}'.format(last_notification))
            # print('[DEBUG] notify at date time is {}'.format(notify_at))
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
    sunny = Meteorologist()
    sunny.check()
