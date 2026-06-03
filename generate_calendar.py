import os
import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

API_TOKEN = os.environ.get('FOOTBALL_DATA_TOKEN', '')
API_URL = "https://api.football-data.org/v4/matches"

def fetch_fixtures():
    headers = {'X-Auth-Token': API_TOKEN}
    params = {'competitions': 'WC'}
    
    if not API_TOKEN:
        return []

    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('matches', [])
    return []

def generate_ics(matches):
    cal = Calendar()
    cal.add('prodid', '-//World Cup 2026 Calendar Generator//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'World Cup 2026')
    cal.add('x-wr-timezone', 'UTC')

    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', 'TBD')
        away_team = match.get('awayTeam', {}).get('name', 'TBD')
        if not home_team: home_team = "TBD"
        if not away_team: away_team = "TBD"
            
        status = match.get('status', 'UNKNOWN')
        start_time_str = match.get('utcDate')
        if not start_time_str: continue
            
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        end_time = start_time + timedelta(hours=2)
        
        event = Event()
        event.add('summary', f"[World Cup] {home_team} vs {away_team}")
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        event.add('dtstamp', datetime.now(pytz.utc))
        event.add('uid', f"match-{match.get('id')}@worldcup2026.app")
        event.add('description', f"Streaming live on Peacock.\nStatus: {status}")
        cal.add_component(event)

    with open('worldcup.ics', 'wb') as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    generate_ics(fetch_fixtures())
