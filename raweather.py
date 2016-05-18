#!/usr/local/bin/python3
import requests
import json
from datetime import datetime as dt
from ratwitter import RaTwitter
from ralogging import RaLogging


class RaWeather():
    """
    Check tomorrows weather for conditions I want to be alerted on
    """

    log = RaLogging()

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
                # self.log.write('Starting Config: {}'.format(self.config))
        except FileNotFoundError:
            errormessage = "[ERROR] Config file not found [{}]".format(self.configfile)
            self.setnotification(errormessage)
            self.sendnotifications()
            self.log.write(errormessage)
            self.log.write(type(self.config))
            exit()
        except json.decoder.JSONDecodeError as jde:
            errormessage = "[ERROR] Error decoding JSON config file"
            self.setnotification(errormessage)
            self.sendnotifications()
            self.log.write(errormessage)
            self.log.write(type(self.config))
            self.log.write(jde)
            exit()

    def loadactivity(self):
        try:
            with open('raweather.activity', 'r') as json_data:
                self.activity = json.load(json_data)
                json_data.close()
                self.log.write('Starting Activity: {}'.format(self.activity))
        except FileNotFoundError:
            errormessage = "[ERROR] Activity file not found"
            self.setnotification(errormessage)
            self.sendnotifications()
            self.log.write(errormessage)
            self.log.write(type(self.activity))
        except json.decoder.JSONDecodeError as jde:
            errormessage = "[ERROR] Error decoding JSON activity file"
            self.setnotification(errormessage)
            self.sendnotifications()
            self.log.write(errormessage)
            self.log.write(type(self.activity))
            self.log.write(jde)
            exit(1)

    def saveactivity(self):
        try:
            with open('raweather.activity', 'w') as json_file:
                json_file.writelines(json.dumps(self.activity))
        except Exception as e:
            self.log.write(e)

    def getweather(self):
        response = requests.get(self.config['wundergroundurl']).json()
        self.alertresponse = requests.get(self.config['wundergroundalerturl']).json()
        # self.log.write(response)
        # self.log.write(self.alertresponse)
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
        lastnotification = dt.strptime(
            self.activity['lastdailynotification']['date'], "%Y-%m-%d %H:%M:%S.%f"
        )
        notificationtimes = self.config['notify']['daily']

        for notifyat in notificationtimes:
            # get notify time with todays date as a datetime object
            # self.log.write("DEBUG {}".format(notifyat))
            notifyatdatetime = dt.strptime(
                str(dt.now().date()) + ' ' + notifyat, '%Y-%m-%d %H:%M'
            )
            # is the configured notification time past, and has no notification already been sent?
            # self.log.write(lastnotification)
            # self.log.write(notifyatdatetime)
            if (dt.now() > notifyatdatetime) and (lastnotification < notifyatdatetime):
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
                        payload = r'{"text": "' + notification['message'] + r'"}'
                        requests.post(self.config['slackposturl'], payload, '\n')

    def check(self):
        weather = self.getweather()
        self.checkweatherconditions(weather)
        self.sendnotifications()
        if self.notificationposted:
            self.activity['lastdailynotification']['message'] = self.lastnotificationpayload
            self.activity['lastdailynotification']['date'] = "{}".format(dt.now())
        self.log.write('Final activity: {}'.format(self.activity))
        self.saveactivity()
        return self.jobresults


if __name__ == '__main__':
    raw = RaWeather()
    raw.check()
