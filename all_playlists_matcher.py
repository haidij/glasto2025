import json

def load_all_playlists():
    """Load all playlist data"""
    with open('all_playlists_artists.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_glastonbury_lineup():
    """Load Glastonbury lineup from JSON file"""
    with open('glastonbury_2025_lineup.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_artists = []
    for stage, days in data.items():
        for day, artists in days.items():
            for artist_info in artists:
                all_artists.append(artist_info['artist'])
    
    return all_artists, data

def normalize_name(name):
    """Simple normalization - just lowercase and remove 'the' prefix"""
    name = name.lower().strip()
    if name.startswith('the '):
        name = name[4:]
    return name

def find_exact_matches(playlists_data, lineup_artists, lineup_data):
    """Find exact matches across all playlists"""
    all_matches = {}
    
    for playlist_name, playlist_data in playlists_data.items():
        matches = []
        
        for playlist_artist in playlist_data['all_artists']:
            norm_playlist = normalize_name(playlist_artist)
            
            for lineup_artist in lineup_artists:
                norm_lineup = normalize_name(lineup_artist)
                
                if norm_playlist == norm_lineup:
                    matches.append({
                        'playlist_artist': playlist_artist,
                        'lineup_artist': lineup_artist
                    })
                    break
        
        if matches:
            all_matches[playlist_name] = matches
    
    return all_matches

def main():
    print("=== GLASTONBURY 2025 - ALL PLAYLISTS MATCHER ===\n")
    
    # Load data
    playlists_data = load_all_playlists()
    glastonbury_artists, lineup_data = load_glastonbury_lineup()
    
    # Find matches
    all_matches = find_exact_matches(playlists_data, glastonbury_artists, lineup_data)
    
    total_matches = sum(len(matches) for matches in all_matches.values())
    
    print(f"Checked {len(playlists_data)} playlists against Glastonbury 2025")
    print(f"Found {total_matches} total exact matches!\n")
    
    if all_matches:
        for playlist_name, matches in all_matches.items():
            print(f"=== {playlist_name.upper()} ({len(matches)} matches) ===")
            
            for match in matches:
                print(f"* {match['playlist_artist']} -> {match['lineup_artist']}")
                
                # Find stage and day info
                for stage, days in lineup_data.items():
                    for day, artists in days.items():
                        for artist_info in artists:
                            if artist_info['artist'] == match['lineup_artist']:
                                print(f"   {stage} - {day} at {artist_info['time']}")
                                break
                print()
            print()
    else:
        print("No exact matches found across all playlists.")
    
    # Create summary schedule
    if all_matches:
        with open('all_playlists_glastonbury_schedule.txt', 'w', encoding='utf-8') as f:
            f.write("GLASTONBURY 2025 - ALL PLAYLISTS SCHEDULE\n")
            f.write("=" * 50 + "\n\n")
            
            # Collect all matches with schedule info
            schedule_matches = []
            for playlist_name, matches in all_matches.items():
                for match in matches:
                    for stage, days in lineup_data.items():
                        for day, artists in days.items():
                            for artist_info in artists:
                                if artist_info['artist'] == match['lineup_artist']:
                                    schedule_matches.append({
                                        'day': day,
                                        'time': artist_info['time'].split(' - ')[0],
                                        'artist': match['lineup_artist'],
                                        'stage': stage,
                                        'playlist': playlist_name
                                    })
                                    break
            
            # Sort by day and time
            day_order = ['Friday 27 June', 'Saturday 28 June', 'Sunday 29 June']
            schedule_matches.sort(key=lambda x: (day_order.index(x['day']), x['time']))
            
            current_day = None
            for match in schedule_matches:
                if match['day'] != current_day:
                    f.write(f"\n{match['day'].upper()}\n")
                    f.write("-" * len(match['day']) + "\n")
                    current_day = match['day']
                
                f.write(f"{match['time']} - {match['artist']} @ {match['stage']} (from '{match['playlist']}')\n")
        
        print(f"Complete schedule saved to: all_playlists_glastonbury_schedule.txt")

if __name__ == "__main__":
    main()