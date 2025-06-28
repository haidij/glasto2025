# Glastonbury 2025 Spotify Playlist Analyzer

A comprehensive toolkit for analyzing your Spotify playlists against the Glastonbury 2025 lineup. Extract artists, find matches, and create your personalized festival schedule!

## 🎵 Features

### Core Tools
- **Single Playlist Analysis** (`spotify_playlist_extractor.py`) - Extract artists from any specific playlist
- **All Playlists Analysis** (`all_playlists_extractor.py`) - Analyze all your playlists at once
- **Glastonbury Matcher** (`all_playlists_matcher.py`) - Find which of your artists are playing at Glastonbury 2025
- **Lineup Converter** (`lineup_converter.py`) - Convert lineup data to structured JSON format

### Analysis Features
- **Artist frequency analysis** - see which artists appear most often
- **Multiple output formats** - JSON with detailed data + simple text lists
- **Festival schedule generation** - create your personalized Glastonbury schedule
- **Cross-playlist matching** - find artists across all your playlists
- **Stage and timing information** - complete festival logistics

### Technical Features
- **Command line or interactive mode** - flexible usage
- **Handles large playlists** - automatic pagination support
- **Case-insensitive search** - finds playlists regardless of capitalization
- **Safe for sharing** - credentials stored separately from code
- **Comprehensive error handling** - helpful error messages and troubleshooting

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Spotify API Access

1. **Create a Spotify App:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Click "Create app"
   - Fill in app details (name and description)
   - Add redirect URI: `http://localhost:8888/callback`
   - Save your app

2. **Get Your Credentials:**
   - Copy your **Client ID** and **Client Secret** from the app dashboard

### 3. Configure Credentials

Create a `secrets.py` file in the project directory:

```python
# Spotify API Credentials
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:8888/callback"
```

**⚠️ Important:** Never commit `secrets.py` to version control! It's already in `.gitignore`.

### 4. Run the Analysis

#### Option A: Analyze a Specific Playlist
```bash
# Interactive mode - you'll be prompted for playlist name
python spotify_playlist_extractor.py

# Command line mode - specify playlist name directly
python spotify_playlist_extractor.py "My Awesome Playlist"
python spotify_playlist_extractor.py "Glastonbury 2025 Wishlist"
```

#### Option B: Analyze All Your Playlists
```bash
# Extract artists from all your playlists
python all_playlists_extractor.py
```

#### Option C: Find Glastonbury Matches
```bash
# First, extract all playlist data
python all_playlists_extractor.py

# Then find matches with Glastonbury 2025 lineup
python all_playlists_matcher.py
```

## 🎪 Glastonbury 2025 Analysis

This toolkit includes the complete Glastonbury 2025 lineup with stage and timing information. The matcher will:

1. **Find exact matches** between your playlist artists and the festival lineup
2. **Show stage and timing details** for each matched artist
3. **Create a personalized schedule** (`all_playlists_glastonbury_schedule.txt`)
4. **Organize by day and time** for easy festival planning

### Example Glastonbury Output
```
=== GLASTONBURY 2025 - ALL PLAYLISTS MATCHER ===

Checked 15 playlists against Glastonbury 2025
Found 23 total exact matches!

=== MY SUMMER HITS (5 matches) ===
* Dua Lipa -> Dua Lipa
   Pyramid Stage - Friday 27 June at 21:30 - 23:00

* Arctic Monkeys -> Arctic Monkeys  
   Pyramid Stage - Saturday 28 June at 21:30 - 23:00
```

## 🔐 First-Time Authentication

The first time you run the script:

1. **Browser will open** - Spotify login page
2. **Log in** with your Spotify account
3. **Authorize the app** - click "Agree" to grant permissions
4. **Copy the redirect URL** - even if you see a connection error, copy the full URL from your browser
5. **Paste into terminal** - the script will extract the authorization code

After this one-time setup, the script will work automatically using cached credentials.

## 📁 Output Files

### Single Playlist Analysis
For a playlist called "My Summer Hits":
- `My_Summer_Hits_artists.json` - Complete data including artist IDs, track names, frequency counts
- `My_Summer_Hits_artists_list.txt` - Simple text list of all unique artists

### All Playlists Analysis
- `all_playlists_artists.json` - Complete data for all your playlists with artist counts and statistics

### Glastonbury Analysis
- `all_playlists_glastonbury_schedule.txt` - Your personalized festival schedule organized by day and time
- Console output showing matches by playlist with stage and timing details

## 💡 Use Cases

- **Festival Preparation:** Create your personalized Glastonbury schedule based on your music taste
- **Playlist Discovery:** Find which artists you listen to most across all playlists
- **Music Analysis:** Discover patterns in your listening habits
- **Concert Planning:** Get organized lists of artists for other festival planning
- **Friend Comparisons:** Share your festival schedule with friends attending Glastonbury

## 🛠️ Troubleshooting

### "Invalid Client" Error
- Check that your `CLIENT_ID` and `CLIENT_SECRET` are correct in `secrets.py`
- Ensure no extra spaces or quotes in the credentials

### "Invalid Redirect URI" Error
- Make sure your Spotify app has exactly this redirect URI: `http://localhost:8888/callback`
- URI must match exactly (including port and path)

### "Playlist Not Found" Error
- Check the exact spelling of your playlist name
- The script will show all available playlists if the target isn't found
- Playlist names are case-insensitive

### Connection Error After Authorization
- This is normal! The browser shows an error, but the script still works
- Just copy the full URL from your browser address bar and paste it into the terminal

## 🔧 Technical Details

- **Language:** Python 3.6+
- **Dependencies:** `spotipy` (Spotify Web API wrapper)
- **Authentication:** OAuth 2.0 Authorization Code Flow
- **Permissions:** Read access to user playlists (public and private)
- **Rate Limiting:** Handled automatically by spotipy
- **Data Sources:** Spotify Web API + Glastonbury 2025 official lineup

## 📊 Included Data

The repository includes the complete Glastonbury 2025 lineup with:
- **All stages:** Pyramid, Other, West Holts, John Peel, Arcadia, etc.
- **Complete schedule:** Friday 27 - Sunday 29 June 2025
- **Timing information:** Start and end times for each performance
- **Structured JSON format:** Easy to parse and extend

## 🚀 Quick Start Example

```bash
# 1. Set up credentials (one-time)
cp secrets.example.py secrets.py
# Edit secrets.py with your Spotify credentials

# 2. Analyze all your playlists
python all_playlists_extractor.py

# 3. Find your Glastonbury matches
python all_playlists_matcher.py

# 4. Check your personalized schedule
cat all_playlists_glastonbury_schedule.txt
```

## 📝 Example Output

```
Looking for playlist: 'Glastonbury Wishlist'...
Found playlist: 'Glastonbury Wishlist' with 127 tracks

Extracting artists from 'Glastonbury Wishlist'...

=== ARTISTS FROM 'Glastonbury Wishlist' ===
Total tracks: 127
Unique artists: 89

Top 10 Most Frequent Artists:
  Arctic Monkeys: 4 track(s)
  Radiohead: 3 track(s)
  The Beatles: 3 track(s)
  Dua Lipa: 2 track(s)
  ...

Data saved to: Glastonbury_Wishlist_artists.json
Artist list also saved to: Glastonbury_Wishlist_artists_list.txt
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool!

## 📄 License

This project is open source. Use it however you'd like!

---

**Happy playlist analyzing! 🎶**
