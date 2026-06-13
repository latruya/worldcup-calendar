import os
import requests
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
    ics_data = "BEGIN:VCALENDAR\r\n"
    ics_data += "VERSION:2.0\r\n"
    ics_data += "PRODID:-//World Cup 2026 Calendar Generator//mxm.dk//\r\n"
    ics_data += "CALSCALE:GREGORIAN\r\n"
    ics_data += "METHOD:PUBLISH\r\n"
    ics_data += "X-WR-CALNAME:World Cup 2026\r\n"
    ics_data += "X-WR-TIMEZONE:UTC\r\n"
    
    # Generate the current time for the mandatory DTSTAMP field
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    
    # Track seen UIDs to prevent any duplicates within the same file
    seen_uids = set()

    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', 'TBD')
        away_team = match.get('awayTeam', {}).get('name', 'TBD')
        date_str = match.get('utcDate')
        
        # Use the stable API match ID - NEVER use uuid4() which changes every run
        match_id = match.get('id')
        if not match_id:
            continue  # Skip matches without a stable ID to avoid duplicates
        
        uid = f"match-{match_id}@worldcup2026.com"
        
        # Skip if we already added this UID (prevents in-file duplicates)
        if uid in seen_uids:
            continue
        seen_uids.add(uid)
        
        if date_str:
            match_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            match_date = match_date.replace(tzinfo=timezone.utc)
            end_date = match_date + timedelta(hours=2)
            
            ics_data += "BEGIN:VEVENT\r\n"
            ics_data += f"UID:{uid}\r\n"
            ics_data += f"DTSTAMP:{now}\r\n"
            ics_data += f"SUMMARY:{home_team} vs {away_team}\r\n"
            ics_data += f"DTSTART:{match_date.strftime('%Y%m%dT%H%M%SZ')}\r\n"
            ics_data += f"DTEND:{end_date.strftime('%Y%m%dT%H%M%SZ')}\r\n"
            ics_data += f"DESCRIPTION:Matchday {match.get('matchday', 'N/A')} - {match.get('stage', 'N/A')}\r\n"
            ics_data += "END:VEVENT\r\n"
            
    ics_data += "END:VCALENDAR\r\n"
    return ics_data.encode('utf-8')

if __name__ == "__main__":
    print("Fetching fixtures...")
    matches = fetch_fixtures()
    print(f"Found {len(matches)} matches.")
    
    ics_data = generate_ics(matches)
    
    with open('worldcup.ics', 'wb') as f:
        f.write(ics_data)
    print("Successfully generated worldcup.ics")