import datetime, re
import googleapiclient.discovery
import google.auth
 
# Preparation for Google API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = 'yukimatsuda.main@gmail.com'
gapi_creds = google.auth.load_credentials_from_file('key.json', SCOPES)[0]
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
 
# Get events from Google Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(
     calendarId=calendar_id, timeMin=now,
     maxResults=5, singleEvents=True,
     orderBy='startTime').execute()
 
# Pick up only start time, end time and summary info
events = events_result.get('items', [])
formatted_events = [(event['start'].get('dateTime', event['start'].get('date')), 
     event['end'].get('dateTime', event['end'].get('date')), 
     event['summary'] if event['summary'] == "講義" else "●"+ event['summary']) for event in events]

 
# Generate output text
response = '[Closest 5 events]\n'

current_date = datetime.datetime.strptime((formatted_events[0])[0], '%Y-%m-%dT%H:%M:%S+09:00').date()

for event in formatted_events:
     if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
         date = datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00').date()
         start_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
         response += '{0} All Day\n{1}\n\n'.format(start_date, event[2])
     # For all day events
     else:
         date = datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00').date()
         start_time = datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00').strftime('%H:%M')
         end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00'))
         if current_date == date:
             response += '{0} ~ {1} {2}\n\n'.format(start_time, end_time, event[2])
         else:
             response += '{0}\n{1} ~ {2} {3}\n\n'.format(date, start_time, end_time, event[2])
             current_date = date
             
response = response.rstrip('\n')
print(response)