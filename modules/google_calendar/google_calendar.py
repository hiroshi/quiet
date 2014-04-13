import argparse
import httplib2
import os, errno, datetime, threading
import apiclient.discovery
import oauth2client.client
import oauth2client.file
import oauth2client.tools
import isodate

# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
# NOTE: *.py files will be archived in site-packages.zip by py2app. So relative to this __file__ don't work.
import __main__
CLIENT_SECRETS = os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), "modules/google_calendar/client_secrets.json")
CACERTS = os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), "modules/google_calendar/cacerts.txt")
# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = oauth2client.client.flow_from_clientsecrets(
  CLIENT_SECRETS,
  scope = [
    #'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.readonly',
  ],
  message = oauth2client.tools.message_if_missing(CLIENT_SECRETS))

def start(app):
  http = httplib2.Http(ca_certs=CACERTS)
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage_path = os.path.expanduser("~/.quiet/modules/google_calendar/oauth2.credentials")
  storage_dir = os.path.dirname(storage_path)
  try:
    os.makedirs(storage_dir)
  except OSError as e:
    if e.errno == errno.EEXIST and os.path.isdir(storage_dir):
      pass
    else:
      raise
  storage = oauth2client.file.Storage(storage_path)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
      # FIXME: Use argparse with no actual aguments
      parser = argparse.ArgumentParser(
          description=__doc__,
          formatter_class=argparse.RawDescriptionHelpFormatter,
          parents=[oauth2client.tools.argparser])
      flags = parser.parse_args([])
      credentials = oauth2client.tools.run_flow(FLOW, storage, flags, http=http)

  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  service = apiclient.discovery.build('calendar', 'v3', http=http)

  #_check_calender_and_update(app, service)
  threading.Timer(0, _check_calender_and_update, args=[app, service, []]).start()


#DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"

def _check_calender_and_update(app, service, items):
  events = []
  now = datetime.datetime.now(tz=isodate.tzinfo.Utc())
  a_day_later = now + datetime.timedelta(days=1)
  try:
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token, showHidden=True).execute()
      for calendar_list_entry in calendar_list['items']:
        if not 'selected' in calendar_list_entry or calendar_list_entry['selected'] == False:
          continue
        #print calendar_list_entry
        calendar_id = calendar_list_entry['id']
        print u"%s (%s)" % (calendar_list_entry['summary'], calendar_id)
        list_response = service.events().list(
            calendarId = calendar_id,
            timeMin = isodate.datetime_isoformat(now),
            timeMax = isodate.datetime_isoformat(now + datetime.timedelta(days=7))
        ).execute()
        for event in list_response['items']:
          if 'recurrence' in event:
            recurrence_events = service.events().instances(
              calendarId = calendar_id,
              eventId = event['id'],
              timeMin = isodate.datetime_isoformat(now),
              timeMax = isodate.datetime_isoformat(now + datetime.timedelta(days=7))
            ).execute()
            for recurrence_event in recurrence_events['items']:
              events.append(recurrence_event)
          else:
            events.append(event)
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
  except oauth2client.client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")
  # get datetime to be sorted
  for event in events:
    if 'date' in event['start']:
      event['_date'] = isodate.parse_date(event['start']['date'])
      event['_datetime'] = datetime.datetime.combine(event['_date'], datetime.time(0, 0, tzinfo=isodate.tzinfo.Utc()))
    if 'dateTime' in event['start']:
      event['_datetime'] = isodate.parse_datetime(event['start']['dateTime'])
  # Display number of events in 24h as "title"
  app.title = len([e for e in events if e['_datetime'] < a_day_later])
  # Clear items added last time
  for item in items:
    del app.menu[item]
  # Display events as menu items
  items = []
  for event in sorted(events, key=lambda e: e['_datetime']):
    start = ""
    if '_date' in event:
      date = event['_date']
      start = "%s/%s %s" % (date.month, date.day, date.strftime("(%a)"))
    elif '_datetime' in event:
      dt = event['_datetime']
      start = "%s/%s %s" % (dt.month, dt.day, dt.strftime("(%a) %H:%M"))
    items.append("%s %s" % (start, event['summary']))
  # Add items
  for item in items:
    app.menu.insert_before('separator_1', item) # FIXME
  #print app.menu

  # Repeat after 5min
  threading.Timer(60 * 5, _check_calender_and_update, args=[app, service, items]).start()

  # tick = int(app.title) + 1
  # print tick
  # app.title = str(tick)
  # threading.Timer(1, timer_func).start()
