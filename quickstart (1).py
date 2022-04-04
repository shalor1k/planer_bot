from __future__ import print_function
import httplib2

import datetime
import os.path
import time
import config

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.client_secret_calendar,
                                                                   'https://www.googleapis.com/auth/calendar')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    count_days = 7
    type_and_name = 'Logotip3'  # создается из названия нажатой кнопки и названием проекта
    start_day = datetime.datetime.now() # Поменять на дату ввеленную юзером
    end_day = start_day
    # if datetime.datetime.isoweekday(end_day) == 6:
    #     end_day = end_day + datetime.timedelta(days=2)
    # if datetime.datetime.isoweekday(end_day) == 7:
    #     end_day = end_day + datetime.timedelta(days=1)
    # end_day = start_day + datetime.timedelta(days=count_days)
    start_data = str(datetime.datetime.now()).split()[0]
    end_data = str(end_day).split()[0]
    # print(end_day)
    for i in range(count_days):
        if datetime.datetime.isoweekday(end_day) == 6:
            end_day = end_day + datetime.timedelta(days=2)
            print('s')
        elif datetime.datetime.isoweekday(end_day) == 7:
            end_day = end_day + datetime.timedelta(days=1)
            print('v')
        else:
            end_day = end_day + datetime.timedelta(days=1)
            print(1)


    end_data = str(end_day).split()[0]

    event = {
        'summary': type_and_name,
        'start': {
            'date': start_data,
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'date': end_data,
            'timeZone': 'Europe/Moscow',
        }
    }
    event = service.events().insert(calendarId='kaltmannmanager@gmail.com', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


    comment = 'disconnect mezdy nami okeani'
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('tasks', 'v1', credentials=creds)
    task = {
        'title': 'New Task1',
        'notes': comment,
        'due': '2022-10-15T12:00:00.000Z',
    }
    print(9)
    event = service.tasks().insert(tasklist='MDk1NzIyOTk3MDg1NjYwODAzODU6MDow', body=task).execute()
    test = event
    event = service.tasks().insert(tasklist='MDk1NzIyOTk3MDg1NjYwODAzODU6MDow', body=task, parent=test.get('id')).execute()
    event = service.tasks().insert(tasklist='MDk1NzIyOTk3MDg1NjYwODAzODU6MDow', body=task,
                                   parent=test.get('id')).execute()
    print('task created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
