import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from collections import Counter

# Configuration - Replace with your credentials
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:8888/callback"

# Spotify API scopes needed
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

def get_user_playlists(sp):
    """Get all user playlists"""
    playlists = []
    results = sp.current_user_playlists(limit=50)
    
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return playlists

def extract_artists_from_playlist(sp, playlist_id):
    """Extract all artists from a specific playlist"""
    artists = []
    
    # Get all tracks from playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Handle pagination
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    # Extract artist information
    for item in tracks:
        if item['track'] and item['track']['artists']:
            for artist in item['track']['artists']:
                artists.append({
                    'name': artist['name'],
                    'id': artist['id'],
                    'track_name': item['track']['name']
                })
    
    return artists

def main():
    try:
        # Initialize Spotify client
        sp = setup_spotify_client()
        
        # Get user playlists
        print("Fetching your playlists...")
        playlists = get_user_playlists(sp)
        
        # Display playlists for selection
        print("\nYour playlists:")
        for i, playlist in enumerate(playlists):
            print(f"{i+1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")
        
        # Get user selection
        while True:
            try:
                choice = int(input(f"\nSelect playlist (1-{len(playlists)}): ")) - 1
                if 0 <= choice < len(playlists):
                    selected_playlist = playlists[choice]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Extract artists from selected playlist
        print(f"\nExtracting artists from '{selected_playlist['name']}'...")
        artists = extract_artists_from_playlist(sp, selected_playlist['id'])
        
        # Count artist occurrences
        artist_counts = Counter([artist['name'] for artist in artists])
        
        # Display results
        print(f"\n=== ARTISTS FROM '{selected_playlist['name']}' ===")
        print(f"Total tracks: {len(artists)}")
        print(f"Unique artists: {len(artist_counts)}")
        
        print("\nTop 10 Most Frequent Artists:")
        for artist, count in artist_counts.most_common(10):
            print(f"  {artist}: {count} track(s)")
        
        print("\nAll Artists (alphabetical):")
        for artist in sorted(set([a['name'] for a in artists])):
            print(f"  - {artist}")
        
        # Save to file
        output_file = f"artists_{selected_playlist['name'].replace(' ', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'playlist_name': selected_playlist['name'],
                'total_tracks': len(artists),
                'unique_artists': len(artist_counts),
                'artist_counts': dict(artist_counts),
                'all_artists': sorted(set([a['name'] for a in artists])),
                'detailed_data': artists
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you've set your CLIENT_ID and CLIENT_SECRET correctly.")

if __name__ == "__main__":
    main()
