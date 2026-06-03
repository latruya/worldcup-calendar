import os
import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

API_TOKEN = os.environ.get('FOOTBALL_DATA_TOKEN', '')
API_URL = "https://api.football-data.org/v4/matches"

def fetch_fixtures():
    headers = {'X-Auth-Token': API_TOKEN}
    # We are using 'PL' (Premier League) here so you can test it with real data immediately!
    # Change 'PL' back to 'WC' when the World Cup 2026 schedule is released.
    params = {'competitions': 'PL'} 
    
    if not API_TOKEN:
        print("Error: API Token not found. Did you add it to GitHub Secrets?")
        return []

    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('matches', [])
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
    return []

def generate_ics(matches):
    cal = Calendar()
    cal.add('prodid', '-//World Cup Calendar Generator//mxm.dk//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Football Calendar')
    cal.add('x-wr-timezone', 'UTC')

    for match in matches:
        # Get start and end times (assuming match lasts ~2 hours)
        start_time = datetime.fromisoformat(match['utcDate'].replace('Z', '+00:00'))
        end_time = start_time + timedelta(hours=2)

        event = Event()
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        status = match['status']
        
        event.add('summary', f"{home_team} vs {away_team}")
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        event.add('dtstamp', datetime.now(pytz.utc))
        event.add('uid', f"match-{match['id']}@football-calendar.local")
        
        # Add scores to description if the match is finished or live
        description = f"Status: {status}\n"
        if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
            score_home = match['score']['fullTime']['home']
            score_away = match['score']['fullTime']['away']
            description += f"Score: {home_team} {score_home} - {score_away} {away_team}\n"
            
        event.add('description', description)
        cal.add_component(event)

    return cal.to_ical()

if __name__ == "__main__":
    print("Fetching fixtures...")
    matches = fetch_fixtures()
    print(f"Found {len(matches)} matches.")
    
    ics_data = generate_ics(matches)
    
    with open('worldcup.ics', 'wb') as f:
        f.write(ics_data)
    print("Successfully generated worldcup.ics")
