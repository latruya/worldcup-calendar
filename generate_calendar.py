import os
import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

# football-data.org constants
API_TOKEN = os.environ.get('FOOTBALL_DATA_TOKEN', '')
API_URL = "https://api.football-data.org/v4/matches"

def fetch_fixtures():
    """Fetch all fixtures for the World Cup."""
    headers = {
        'X-Auth-Token': API_TOKEN
    }
    params = {
        'competitions': 'WC'
    }
    
    if not API_TOKEN:
        print("Warning: FOOTBALL_DATA_TOKEN not set. Cannot fetch live data.")
        return []

    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('matches', [])
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        return []

def generate_ics(matches):
    """Generate an ICS file compatible with Outlook."""
    cal = Calendar()
    cal.add('prodid', '-//World Cup 2026 Calendar Generator//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'World Cup 2026 (Peacock)')
    cal.add('x-wr-timezone', 'UTC')
    cal.add('x-wr-caldesc', 'Live updating World Cup 2026 Schedule')

    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', 'TBD')
        away_team = match.get('awayTeam', {}).get('name', 'TBD')
        
        # Sometimes teams are empty before group stages are fully decided
        if not home_team: home_team = "TBD"
        if not away_team: away_team = "TBD"
            
        status = match.get('status', 'UNKNOWN')
        stage = match.get('stage', 'Match').replace('_', ' ').title()
        
        # Time parsing (football-data.org returns UTC with Z)
        start_time_str = match.get('utcDate')
        if not start_time_str:
            continue
            
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        end_time = start_time + timedelta(hours=2)
        
        event = Event()
        summary = f"[{stage}] {home_team} vs {away_team}"
        
        event.add('summary', summary)
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        event.add('dtstamp', datetime.now(pytz.utc))
        
        event_uid = f"match-{match.get('id')}@worldcup2026.app"
        event.add('uid', event_uid)
        
        description = "Streaming live on Peacock.\n\n"
        description += f"Status: {status}\n"
        
        event.add('description', description)
        cal.add_component(event)

    with open('worldcup.ics', 'wb') as f:
        f.write(cal.to_ical())
        
    print(f"Generated worldcup.ics with {len(matches)} events.")

def main():
    print("Fetching World Cup matches from football-data.org...")
    matches = fetch_fixtures()
    if matches:
        generate_ics(matches)
    else:
        print("Creating an empty calendar template since no data was fetched.")
        generate_ics([])

if __name__ == "__main__":
    main()
