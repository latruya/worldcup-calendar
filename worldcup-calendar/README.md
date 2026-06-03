# World Cup 2026 Dynamic Calendar Feed

This project generates an auto-updating `.ics` calendar feed for the 2026 World Cup, perfectly compatible with Microsoft Outlook and other calendar apps. It fetches live data from football-data.org to automatically update knockout stage teams (the "TBDs") as they are decided.

## Setup Instructions

### 1. Get an API Key
You need a free API key to pull live match data.
1. Go to [football-data.org](https://www.football-data.org/).
2. Click on **Get your API key**.
3. Register with your name and email.
4. Check your email for your API Token (it's a string of letters and numbers).

### 2. Push to GitHub
1. Create a new repository on your GitHub account.
2. Upload all the files from this directory (`generate_calendar.py`, `requirements.txt`, `.github/workflows/update_calendar.yml`) to your repository.

### 3. Add GitHub Secret
To allow GitHub Actions to fetch data, add your API key securely:
1. Go to your repository's **Settings** tab.
2. Navigate to **Secrets and variables** -> **Actions**.
3. Click **New repository secret**.
4. Name: `FOOTBALL_DATA_TOKEN`
5. Secret: Paste the API Token you received in your email from Step 1.
6. Click **Add secret**.

### 4. Run the Action
1. Go to the **Actions** tab in your repository.
2. Select "Update World Cup Calendar" from the left sidebar.
3. Click **Run workflow** -> **Run workflow** to trigger the first data fetch.
4. Once it finishes, a new file `worldcup.ics` will appear in your repository.

### 5. Subscribe in Outlook
1. In your GitHub repository, click on the `worldcup.ics` file.
2. Click the **Raw** button. This will open a page with plain text.
3. Copy the URL from your browser's address bar (it will start with `https://raw.githubusercontent.com/...`).
4. Open **Outlook**.
5. Go to your Calendar.
6. Click **Add Calendar** -> **Subscribe from web** (or "From Internet" on desktop).
7. Paste the URL and click **Import**.

Whenever a match outcome updates the schedule, GitHub Actions will automatically update the `worldcup.ics` file every 12 hours, and Outlook will automatically pull the newest schedule!
