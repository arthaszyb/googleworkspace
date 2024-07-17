# Import libraries
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

# Define spreadsheet details (replace with yours)
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # Replace with your Google Sheet ID
SHEET_NAME = 'Sheet1'  # Replace with the sheet name containing event data

# Define Google Calendar API details
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Replace with path to your credentials file

def get_events_from_sheet():
  """Reads event list from the Google Sheet."""
  # Setup Google Sheet API service
  credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
  service = build('sheets', 'v4', credentials=credentials)

  # Read data from the sheet
  sheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                              range=f'{SHEET_NAME}!A1:F').execute()
  values = sheet.get('values', [])

  # Extract event data (assuming headers are in the first row)
  events = []
  headers = values[0] if values else []
  for row in values[1:]:
    event = dict(zip(headers, row))
    events.append(event)
  return events

def create_calendar_event(event):
  """Creates a Google Calendar event based on event data."""
  # Extract event details
  start_date = event['Start Date']
  end_date = event['End Date']
  title = event['Title']
  description = event.get('Description', '')

  # Prepare event body
  event_body = {
      'summary': title,
      'description': description,
      'start': {
          'date': start_date,
      },
      'end': {
          'date': end_date,
      },
  }

  # Setup Google Calendar API service (same as above)
  credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
  service = build('calendar', 'v3', credentials=credentials)

  # Insert event to calendar
  event = service.events().insert(calendarId='primary', body=event_body).execute()
  print(f"Event created: {event.get('htmlLink')}")

if __name__ == '__main__':
  events = get_events_from_ sheet()
  for event in events:
    create_calendar_event(event)
