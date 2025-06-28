import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

SCOPE = "playlist-read-private playlist-read-collaborative"

def setup_spotify_client():
    """Initialize Spotify client with authentication"""
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def get_artist_id(sp, artist_name):
    """Get Spotify ID for an artist"""
    try:
        results = sp.search(q=artist_name, type='artist', limit=1)
        if results['artists']['items']:
            return results['artists']['items'][0]['id']
    except:
        pass
    return None

def get_related_artists(sp, artist_id):
    """Get related artists for a given artist"""
    try:
        related = sp.artist_related_artists(artist_id)
        return [artist['name'] for artist in related['artists']]
    except:
        return []

def load_glastonbury_lineup():
    """Load Glastonbury lineup"""
    with open('glastonbury_2025_lineup.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_artists = []
    for stage, days in data.items():
        for day, artists in days.items():
            for artist_info in artists:
                all_artists.append(artist_info['artist'])
    
    return all_artists, data

def normalize_name(name):
    """Normalize artist names for matching"""
    return name.lower().strip().replace('the ', '')

def main():
    print("=== GLASTONBURY 2025 - RELATED ARTISTS FINDER ===\n")
    
    # Load your existing matches
    with open('all_playlists_artists.json', 'r', encoding='utf-8') as f:
        playlists_data = json.load(f)
    
    # Get artists you already have matches for
    known_matches = ['Caribou', 'Gracie Abrams', 'Maribou State', 'RAYE', 'The Maccabees', 'Tom Odell', 'Turnstile', 'Billy Bragg']
    
    # Load Glastonbury lineup
    glastonbury_artists, lineup_data = load_glastonbury_lineup()
    
    # Setup Spotify client
    sp = setup_spotify_client()
    
    print("Finding related artists for your Glastonbury matches...")
    
    all_related = set()
    
    # Get related artists for each of your matches
    for match_artist in known_matches:
        print(f"Getting related artists for {match_artist}...")
        artist_id = get_artist_id(sp, match_artist)
        
        if artist_id:
            related = get_related_artists(sp, artist_id)
            all_related.update(related)
            print(f"  Found {len(related)} related artists")
    
    print(f"\nTotal related artists found: {len(all_related)}")
    
    # Find which related artists are at Glastonbury
    glastonbury_suggestions = []
    
    for related_artist in all_related:
        norm_related = normalize_name(related_artist)
        
        for glasto_artist in glastonbury_artists:
            norm_glasto = normalize_name(glasto_artist)
            
            if norm_related == norm_glasto and glasto_artist not in known_matches:
                # Find stage and day info
                for stage, days in lineup_data.items():
                    for day, artists in days.items():
                        for artist_info in artists:
                            if artist_info['artist'] == glasto_artist:
                                glastonbury_suggestions.append({
                                    'artist': glasto_artist,
                                    'stage': stage,
                                    'day': day,
                                    'time': artist_info['time']
                                })
                                break
                break
    
    print(f"\n=== GLASTONBURY ARTISTS YOU MIGHT LIKE ===")
    print(f"Based on artists similar to your matches, found {len(glastonbury_suggestions)} suggestions:\n")
    
    if glastonbury_suggestions:
        for suggestion in glastonbury_suggestions:
            print(f"* {suggestion['artist']}")
            print(f"   {suggestion['stage']} - {suggestion['day']} at {suggestion['time']}")
            print()
        
        # Save suggestions
        with open('glastonbury_suggestions.json', 'w', encoding='utf-8') as f:
            json.dump(glastonbury_suggestions, f, indent=2, ensure_ascii=False)
        
        print(f"Suggestions saved to: glastonbury_suggestions.json")
    else:
        print("No new Glastonbury artists found in related artists.")

if __name__ == "__main__":
    main()