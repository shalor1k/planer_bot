from __future__ import print_function
import httplib2

import pickle
import datetime
import requests
import json

import os.path
import config

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main(time_delta, name, comment, date):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(config.client_secret_calendar,
                                                                       'https://www.googleapis.com/auth/calendar')
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        count_days = time_delta
        type_and_name = name  # создаётся из названия нажатой кнопки и названием проекта

        end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
        end_day = datetime.datetime.fromisoformat(end_data)
        end_day = end_day + datetime.timedelta(days=time_delta)
        start_date = date[0:8] + str(date[8:]) + ' 12:00:00.000'
        start_day = datetime.datetime.fromisoformat(end_data)
        if datetime.datetime.isoweekday(end_day) == 6:
            end_day = end_day + datetime.timedelta(days=2)
            print('s')
        elif datetime.datetime.isoweekday(end_day) == 7:
            end_day = end_day + datetime.timedelta(days=2)
            print('v')
        else:
            end_day = end_day + datetime.timedelta(days=2)
            print(1)

        if datetime.datetime.isoweekday(start_day) == 7:
            if time_delta == 7:
                end_day = end_day + datetime.timedelta(days=1)

            if time_delta == 15:
                end_day = end_day + datetime.timedelta(days=3)

        if datetime.datetime.isoweekday(start_day) == 6:
            if time_delta == 7:
                end_day = end_day + datetime.timedelta(days=2)

        if datetime.datetime.isoweekday(start_day) == 5:
            if time_delta == 7:
                end_day = end_day + datetime.timedelta(days=2)
            elif time_delta == 15:
                end_day = end_day + datetime.timedelta(days=4)
            elif time_delta == 20:
                end_day = end_day + datetime.timedelta(days=6)

        if datetime.datetime.isoweekday(start_day) == 1:
            if time_delta == 20:
                end_day = end_day + datetime.timedelta(days=-2)
            elif time_delta == 15:
                end_day = end_day + datetime.timedelta(days=2)

            elif time_delta == 5:
                end_day = end_day + datetime.timedelta(days=-2)

        elif datetime.datetime.isoweekday(start_day) == 4:
            if time_delta == 15:
                end_day = end_day + datetime.timedelta(days=4)

        elif datetime.datetime.isoweekday(start_day) == 3:
            if time_delta == 15:
                end_day = end_day + datetime.timedelta(days=4)

        elif datetime.datetime.isoweekday(start_day) == 2 or datetime.datetime.isoweekday(start_day) == 6:
            if time_delta == 15:
                end_day = end_day + datetime.timedelta(days=4)

        elif datetime.datetime.isoweekday(start_day) == 7:
            if time_delta == 20 or time_delta == 5:
                end_day = end_day + datetime.timedelta(days=-1)

        if time_delta == 20 and datetime.datetime.isoweekday(start_day) != 5:
            end_day = end_day + datetime.timedelta(days=6)

        event = {
            'summary': type_and_name,
            'start': {
                'date': str(datetime.datetime.fromisoformat(str(date))).split()[0],
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'date': str(end_day).split()[0],
                'timeZone': 'Europe/Moscow',
            }
        }
        event = service.events().insert(calendarId='mail', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', 'https://www.googleapis.com/auth/tasks')
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials1.json', 'https://www.googleapis.com/auth/tasks')
                authorization_url, state = flow.authorization_url(
                    access_type='offline',
                    login_hint='mail',
                    include_granted_scopes='true')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials1.json', 'https://www.googleapis.com/auth/tasks', state=state)
                creds = flow.run_local_server(port=0)
                print(2)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        delta = 0

        if time_delta == 7:
            if 1 <= datetime.datetime.isoweekday(start_day) <= 7:
                delta -= 8

        elif time_delta == 20:
            if 1<= datetime.datetime.isoweekday(start_day) <= 7:
                delta -= 21

        elif time_delta == 5:
            if 1 <= datetime.datetime.isoweekday(start_day) <= 7:
                delta -= 6

        elif time_delta == 15:
            if 1 <= datetime.datetime.isoweekday(start_day) <= 7:
                delta -= 16

        service = build('tasks', 'v1', credentials=creds)
        end_task_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
        end_task_day = datetime.datetime.fromisoformat(end_task_data)
        end_day = end_day + datetime.timedelta(days=time_delta + delta)
        end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        task = {
            'title': str(name),
            'notes': str(comment),
            'due': end_day,
        }
        print(task)
        event = service.tasks().insert(tasklist='***', body=task).execute()
        test = event

        if time_delta == 7:
            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=5)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 2

            if datetime.datetime.isoweekday(start_day) == 5:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 3:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 4:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 3

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_third = {
                'title': str(name) + ' 3/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_third,
                                           parent=test.get('id')).execute()
            print(event)
            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=3)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 4:
                delta += 1

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 1

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_second = {
                'title': str(name) + ' 2/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_second,
                                           parent=test.get('id')).execute()
            print(event)

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=1)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 6:
                delta += 1

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 1

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_first = {
                'title': str(name) + ' 1/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_first,
                                           parent=test.get('id')).execute()
            print(event)

        elif time_delta == 15:

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=13)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta += 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta += 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 4\
                    or datetime.datetime.isoweekday(start_day) == 3 or datetime.datetime.isoweekday(start_day) == 6:
                delta += 6

            elif datetime.datetime.isoweekday(start_day) == 2:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 1 or datetime.datetime.isoweekday(start_day) == 7:
                delta += 3

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_second = {
                'title': str(name) + ' Выгрузка',
                'notes': '',
                'due': end_day,
            }

            event = service.tasks().insert(tasklist='***', body=task_second,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=9)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta += 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta += 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 7:
                delta += 3

            elif datetime.datetime.isoweekday(start_day) == 4 or datetime.datetime.isoweekday(start_day) == 1:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 3 or datetime.datetime.isoweekday(start_day) == 2\
                    or datetime.datetime.isoweekday(start_day) == 6:
                delta += 4

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_first = {
                'title': str(name) + ' Согласование',
                'notes': '',
                'due': end_day,
            }

            event = service.tasks().insert(tasklist='***', body=task_first,
                                           parent=test.get('id')).execute()

        elif time_delta == 20:

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=18)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5:
                delta += 8

            elif datetime.datetime.isoweekday(start_day) == 4:
                delta += 8

            elif datetime.datetime.isoweekday(start_day) == 3:
                delta += 7

            elif datetime.datetime.isoweekday(start_day) == 2:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 1:
                delta += 6

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 8

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 7

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_seventh = {
                'title': str(name) + ' Выгрузка проекта',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_seventh,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=16)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 7:
                delta += 7

            elif datetime.datetime.isoweekday(start_day) == 4:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 3 or datetime.datetime.isoweekday(start_day) == 2 \
                    or datetime.datetime.isoweekday(start_day) == 1:
                delta += 6

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 8

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_sixth = {
                'title': str(name) + ' Согласование фирстиля',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_sixth,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=11)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 6:
                delta += 6

            elif datetime.datetime.isoweekday(start_day) == 4 or datetime.datetime.isoweekday(start_day) == 1:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 3:
                delta += 3

            elif datetime.datetime.isoweekday(start_day) == 2:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 5

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_fifth = {
                'title': str(name) + ' Логотип 3/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_fifth,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=9)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5:
                delta += 3

            elif datetime.datetime.isoweekday(start_day) == 4:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 3 or datetime.datetime.isoweekday(start_day) == 2\
                    or datetime.datetime.isoweekday(start_day) == 6:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 1:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 3

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_fourth = {
                'title': str(name) + ' Логотип 2/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_fourth,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=7)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 4:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 3 or datetime.datetime.isoweekday(start_day) == 2 \
                    or datetime.datetime.isoweekday(start_day) == 1 or datetime.datetime.isoweekday(start_day) == 6\
                    or datetime.datetime.isoweekday(start_day) == 7:
                delta += 2

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_third = {
                'title': str(name) + ' Логотип 1/3',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_third,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=5)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5 or datetime.datetime.isoweekday(start_day) == 4 \
                    or datetime.datetime.isoweekday(start_day) == 3:
                delta += 2

            elif datetime.datetime.isoweekday(start_day) == 2:
                delta += 1

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 4

            elif datetime.datetime.isoweekday(start_day) == 7:
                delta += 3

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_second = {
                'title': str(name) + ' Слоган',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_second,
                                           parent=test.get('id')).execute()

            delta = 0
            end_data = date[0:8] + str(date[8:]) + ' 12:00:00.000'
            end_day = datetime.datetime.fromisoformat(end_data)
            end_day = end_day + datetime.timedelta(days=2)
            if datetime.datetime.isoweekday(end_day) == 6:
                delta = 2
            elif datetime.datetime.isoweekday(end_day) == 7:
                delta = 1

            if datetime.datetime.isoweekday(start_day) == 5:
                delta += 1

            elif datetime.datetime.isoweekday(start_day) == 2 or datetime.datetime.isoweekday(start_day) == 7:
                delta += 1

            elif datetime.datetime.isoweekday(start_day) == 6:
                delta += 2

            end_day = end_day + datetime.timedelta(days=delta)
            end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S.000Z")

            task_first = {
                'title': str(name) + ' Нейминг',
                'notes': '',
                'due': end_day,
            }
            event = service.tasks().insert(tasklist='***', body=task_first,
                                           parent=test.get('id')).execute()

            print('task created: %s' % (event.get('htmlLink')))

    except Exception:
        params = {
            "grant_type": "refresh_token",
            "client_id": "id",
            "client_secret": "secret",
            "refresh_token": "token"
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
            print(r.json()['access_token'])
            tok = str(r.json()['access_token'])
            with open('token.json', "rt", encoding="utf-8") as f:
                data = json.load(f)
            data['token'] = tok
            with open("token.json", "wt", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        else:
            print("Error")


# main(5, 'logo', 'comm', '2022-02-06')
