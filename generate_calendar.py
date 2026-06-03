import os
import requests
import uuid
from datetime import datetime, timedelta, timezone

def fetch_fixtures():
    token = os.environ.get('FOOTBALL_DATA_TOKEN')
    if not token:
        print("Error: API Token not found. Did you add it to GitHub Secrets?")
        return []
    
    headers = {
        'X-Auth-Token': token
    }
    try:
        url = 'https://api.football-data.org/v4/competitions/WC/matches'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('matches', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def generate_ics(matches):
    ics_data = "BEGIN:VCALENDAR\n"
    ics_data += "VERSION:2.0\n"
    ics_data += "PRODID:-//World Cup 2026 Calendar Generator//mxm.dk//\n"
    ics_data += "CALSCALE:GREGORIAN\n"
    ics_data += "METHOD:PUBLISH\n"
    ics_data += "X-WR-CALNAME:World Cup 2026\n"
    ics_data += "X-WR-TIMEZONE:UTC\n"
    
    # Generate the current time for the mandatory DTSTAMP field
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    
    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', 'TBD')
        away_team = match.get('awayTeam', {}).get('name', 'TBD')
        date_str = match.get('utcDate')
        
        # Use the API's match ID, or generate a random one if it doesn't exist
        match_id = match.get('id', uuid.uuid4())
        
        if date_str:
            match_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            end_date = match_date + timedelta(hours=2)
            
            ics_data += "BEGIN:VEVENT\n"
            ics_data += f"UID:match-{match_id}@worldcup2026.com\n"
            ics_data += f"DTSTAMP:{now}\n"
            ics_data += f"SUMMARY:{home_team} vs {away_team}\n"
            ics_data += f"DTSTART:{match_date.strftime('%Y%m%dT%H%M%SZ')}\n"
            ics_data += f"DTEND:{end_date.strftime('%Y%m%dT%H%M%SZ')}\n"
            ics_data += f"DESCRIPTION:Matchday {match.get('matchday', 'N/A')} - {match.get('stage', 'N/A')}\n"
            ics_data += "END:VEVENT\n"
            
    ics_data += "END:VCALENDAR\n"
    return ics_data.encode('utf-8')

if __name__ == "__main__":
    print("Fetching fixtures...")
    matches = fetch_fixtures()
    print(f"Found {len(matches)} matches.")
    
    ics_data = generate_ics(matches)
    
    with open('worldcup.ics', 'wb') as f:
        f.write(ics_data)
    print("Successfully generated worldcup.ics")
