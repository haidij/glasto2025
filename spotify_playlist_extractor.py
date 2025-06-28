import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import sys
from collections import Counter
from secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

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

def find_playlist_by_name(sp, playlist_name):
    """Find a specific playlist by name"""
    results = sp.current_user_playlists(limit=50)
    
    while results:
        for playlist in results['items']:
            if playlist['name'].lower() == playlist_name.lower():
                return playlist
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return None

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
        # Get playlist name from command line or user input
        if len(sys.argv) > 1:
            playlist_name = " ".join(sys.argv[1:])
        else:
            playlist_name = input("Enter playlist name: ").strip()
        
        if not playlist_name:
            print("No playlist name provided!")
            return
        
        # Initialize Spotify client
        sp = setup_spotify_client()
        
        # Find the specific playlist
        print(f"Looking for playlist: '{playlist_name}'...")
        
        playlist = find_playlist_by_name(sp, playlist_name)
        
        if not playlist:
            print(f"Playlist '{playlist_name}' not found!")
            print("\nAvailable playlists:")
            playlists = sp.current_user_playlists(limit=50)
            for p in playlists['items']:
                print(f"  - {p['name']}")
            return
        
        print(f"Found playlist: '{playlist['name']}' with {playlist['tracks']['total']} tracks")
        
        # Extract artists from the playlist
        print(f"\nExtracting artists from '{playlist['name']}'...")
        artists = extract_artists_from_playlist(sp, playlist['id'])
        
        # Count artist occurrences
        artist_counts = Counter([artist['name'] for artist in artists])
        
        # Display results
        print(f"\n=== ARTISTS FROM '{playlist['name']}' ===")
        print(f"Total tracks: {len(artists)}")
        print(f"Unique artists: {len(artist_counts)}")
        
        print("\nTop 10 Most Frequent Artists:")
        for artist, count in artist_counts.most_common(10):
            print(f"  {artist}: {count} track(s)")
        
        print("\nAll Artists (alphabetical):")
        for artist in sorted(set([a['name'] for a in artists])):
            print(f"  - {artist}")
        
        # Create safe filename
        safe_name = playlist['name'].replace(' ', '_').replace('/', '_').replace('\\', '_')
        
        # Save to file
        output_file = f"{safe_name}_artists.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'playlist_name': playlist['name'],
                'total_tracks': len(artists),
                'unique_artists': len(artist_counts),
                'artist_counts': dict(artist_counts),
                'all_artists': sorted(set([a['name'] for a in artists])),
                'detailed_data': artists
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to: {output_file}")
        
        # Also create a simple text file with just artist names
        text_file = f"{safe_name}_artists_list.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"Artists from '{playlist['name']}'\n")
            f.write("=" * 50 + "\n\n")
            for artist in sorted(set([a['name'] for a in artists])):
                f.write(f"{artist}\n")
        
        print(f"Artist list also saved to: {text_file}")
        
    except ImportError:
        print("Error: secrets.py file not found!")
        print("Please create secrets.py with your Spotify API credentials.")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you've set your credentials correctly in secrets.py")

if __name__ == "__main__":
    main()
