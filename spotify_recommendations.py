import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import random
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

def get_artist_ids(sp, artist_names):
    """Get Spotify IDs for artists"""
    artist_ids = []
    for name in artist_names[:5]:  # Limit to 5 seed artists
        try:
            results = sp.search(q=name, type='artist', limit=1)
            if results['artists']['items']:
                artist_ids.append(results['artists']['items'][0]['id'])
        except:
            continue
    return artist_ids

def get_recommendations(sp, seed_artists):
    """Get recommendations based on seed artists"""
    try:
        recommendations = sp.recommendations(seed_artists=seed_artists, limit=50)
        return recommendations['tracks']
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
    print("=== GLASTONBURY 2025 RECOMMENDATIONS ===\n")
    
    # Load your playlist data
    with open('all_playlists_artists.json', 'r', encoding='utf-8') as f:
        playlists_data = json.load(f)
    
    # Get all unique artists from your playlists
    all_your_artists = set()
    for playlist_data in playlists_data.values():
        all_your_artists.update(playlist_data['all_artists'])
    
    print(f"Found {len(all_your_artists)} unique artists in your playlists")
    
    # Load Glastonbury lineup
    glastonbury_artists, lineup_data = load_glastonbury_lineup()
    
    # Setup Spotify client
    sp = setup_spotify_client()
    
    # Get recommendations based on your top artists
    top_artists = list(all_your_artists)[:50]  # Use top 50 artists
    random.shuffle(top_artists)
    
    print("Getting Spotify recommendations...")
    
    # Get artist IDs for seeds
    seed_artist_ids = get_artist_ids(sp, top_artists[:5])
    
    if not seed_artist_ids:
        print("Could not find seed artists on Spotify")
        return
    
    # Get recommendations
    recommendations = get_recommendations(sp, seed_artist_ids)
    
    if not recommendations:
        print("No recommendations found")
        return
    
    # Extract recommended artist names
    recommended_artists = []
    for track in recommendations:
        for artist in track['artists']:
            recommended_artists.append(artist['name'])
    
    # Find which recommended artists are at Glastonbury
    glastonbury_recommendations = []
    
    for rec_artist in set(recommended_artists):
        norm_rec = normalize_name(rec_artist)
        
        for glasto_artist in glastonbury_artists:
            norm_glasto = normalize_name(glasto_artist)
            
            if norm_rec == norm_glasto:
                # Find stage and day info
                for stage, days in lineup_data.items():
                    for day, artists in days.items():
                        for artist_info in artists:
                            if artist_info['artist'] == glasto_artist:
                                glastonbury_recommendations.append({
                                    'artist': glasto_artist,
                                    'stage': stage,
                                    'day': day,
                                    'time': artist_info['time']
                                })
                                break
                break
    
    print(f"\n=== GLASTONBURY ARTISTS YOU MIGHT LIKE ===")
    print(f"Based on your listening history, found {len(glastonbury_recommendations)} recommendations:\n")
    
    if glastonbury_recommendations:
        for rec in glastonbury_recommendations:
            print(f"* {rec['artist']}")
            print(f"   {rec['stage']} - {rec['day']} at {rec['time']}")
            print()
        
        # Save recommendations
        with open('glastonbury_recommendations.json', 'w', encoding='utf-8') as f:
            json.dump(glastonbury_recommendations, f, indent=2, ensure_ascii=False)
        
        print(f"Recommendations saved to: glastonbury_recommendations.json")
    else:
        print("No Glastonbury artists found in your recommendations.")
        print("This could mean:")
        print("- Your taste is quite unique!")
        print("- The recommendation algorithm didn't find matches")
        print("- Try running again for different seed artists")

if __name__ == "__main__":
    main()