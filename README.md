# Glastonbury 2025 Playlist Matcher

Match your Spotify playlist artists with Glastonbury 2025 lineup and identify which acts will be broadcast on TV/iPlayer.

## Setup

1. **Install dependencies:**
   ```bash
   pip install spotipy requests
   ```

2. **Create Spotify App:**
   - Go to https://developer.spotify.com/dashboard
   - Create a new app
   - Use redirect URI: `http://localhost:8888/callback`

3. **Add your credentials:**
   - Copy your Client ID and Client Secret
   - Create `secrets.py` with:
   ```python
   CLIENT_ID = "your_client_id"
   CLIENT_SECRET = "your_client_secret"
   REDIRECT_URI = "http://localhost:8888/callback"
   ```

## Usage

1. **Extract all your playlists:**
   ```bash
   python all_playlists_extractor.py
   ```

2. **Find Glastonbury matches:**
   ```bash
   python broadcast_matcher.py
   ```

## Output Files

- `all_playlists_artists.json` - All artists from your Spotify playlists
- `broadcast_schedule.txt` - Your artists that will be broadcast on TV/iPlayer
- `complete_festival_schedule.txt` - Complete schedule (broadcast + festival-only)
- `glastonbury_2025_lineup.json` - Full festival lineup with broadcast info

## Features

- **Exact matching** - Only finds genuine artist matches (no false positives)
- **Broadcast identification** - Separates TV coverage from festival-only acts
- **Multi-playlist support** - Analyzes all your Spotify playlists at once
- **Schedule generation** - Creates personalized festival schedules
- **Glastonbury 2025 data** - Complete lineup with stage and timing info

## Key Scripts

- `all_playlists_extractor.py` - Extract artists from all your playlists
- `broadcast_matcher.py` - Match artists and identify broadcast coverage
- `spotify_playlist_extractor.py` - Extract artists from individual playlists
- `lineup_converter.py` - Convert lineup data to JSON format

## Results

The matcher identifies which of your favorite artists are performing at Glastonbury 2025 and tells you:
- Which performances will be broadcast on TV/BBC iPlayer
- Which acts require festival attendance to see
- Complete schedule with stages and times