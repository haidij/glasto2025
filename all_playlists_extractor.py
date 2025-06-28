import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from collections import Counter
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

def extract_artists_from_playlist(sp, playlist_id):
    """Extract all artists from a specific playlist"""
    artists = []
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    for item in tracks:
        if item['track'] and item['track']['artists']:
            for artist in item['track']['artists']:
                artists.append(artist['name'])
    
    return artists

def get_all_playlists_artists(sp):
    """Get artists from all user playlists"""
    all_data = {}
    
    results = sp.current_user_playlists(limit=50)
    
    while results:
        for playlist in results['items']:
            if playlist['owner']['id'] == sp.me()['id']:  # Only user's own playlists
                print(f"Processing playlist: '{playlist['name']}'...")
                
                artists = extract_artists_from_playlist(sp, playlist['id'])
                unique_artists = sorted(set(artists))
                artist_counts = Counter(artists)
                
                all_data[playlist['name']] = {
                    'playlist_name': playlist['name'],
                    'total_tracks': len(artists),
                    'unique_artists': len(unique_artists),
                    'artist_counts': dict(artist_counts),
                    'all_artists': unique_artists
                }
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return all_data

def main():
    try:
        sp = setup_spotify_client()
        
        print("Extracting artists from all your playlists...")
        all_playlists_data = get_all_playlists_artists(sp)
        
        # Save to JSON file
        with open('all_playlists_artists.json', 'w', encoding='utf-8') as f:
            json.dump(all_playlists_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nProcessed {len(all_playlists_data)} playlists:")
        for name, data in all_playlists_data.items():
            print(f"  - {name}: {data['unique_artists']} unique artists")
        
        print(f"\nData saved to: all_playlists_artists.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()