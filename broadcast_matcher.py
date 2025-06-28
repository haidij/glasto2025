import json

def load_all_playlists():
    """Load all playlist data"""
    with open('all_playlists_artists.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_glastonbury_lineup():
    """Load Glastonbury lineup from JSON file"""
    with open('glastonbury_2025_lineup.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_name(name):
    """Simple normalization - just lowercase and remove 'the' prefix"""
    name = name.lower().strip()
    if name.startswith('the '):
        name = name[4:]
    return name

def find_exact_matches(playlists_data, lineup_data):
    """Find exact matches and separate by broadcast status"""
    # Get all unique artists from playlists
    all_your_artists = set()
    for playlist_data in playlists_data.values():
        all_your_artists.update(playlist_data['all_artists'])
    
    broadcast_matches = []
    non_broadcast_matches = []
    
    for stage, days in lineup_data.items():
        is_broadcast = "(broadcast)" in stage
        
        for day, artists in days.items():
            for artist_info in artists:
                lineup_artist = artist_info['artist']
                norm_lineup = normalize_name(lineup_artist)
                
                for playlist_artist in all_your_artists:
                    norm_playlist = normalize_name(playlist_artist)
                    
                    if norm_playlist == norm_lineup:
                        match_info = {
                            'playlist_artist': playlist_artist,
                            'lineup_artist': lineup_artist,
                            'stage': stage.replace(' (broadcast)', ''),
                            'day': day,
                            'time': artist_info['time'],
                            'broadcast': is_broadcast
                        }
                        
                        if is_broadcast:
                            broadcast_matches.append(match_info)
                        else:
                            non_broadcast_matches.append(match_info)
                        break
    
    return broadcast_matches, non_broadcast_matches

def main():
    print("=== GLASTONBURY 2025 - BROADCAST vs NON-BROADCAST MATCHES ===\n")
    
    # Load data
    playlists_data = load_all_playlists()
    lineup_data = load_glastonbury_lineup()
    
    # Find matches
    broadcast_matches, non_broadcast_matches = find_exact_matches(playlists_data, lineup_data)
    
    total_matches = len(broadcast_matches) + len(non_broadcast_matches)
    
    print(f"Found {total_matches} total exact matches!")
    print(f"  - {len(broadcast_matches)} will be broadcast on TV/iPlayer")
    print(f"  - {len(non_broadcast_matches)} are not being broadcast\n")
    
    if broadcast_matches:
        print("=== BROADCAST ACTS (TV/iPlayer Coverage) ===")
        
        # Sort by day and time
        day_order = ['Friday', 'Saturday', 'Sunday']
        broadcast_matches.sort(key=lambda x: (day_order.index(x['day']) if x['day'] in day_order else 99, x['time']))
        
        for match in broadcast_matches:
            print(f"* {match['lineup_artist']}")
            print(f"   {match['stage']} - {match['day']} at {match['time']}")
            print(f"   [BROADCAST] Will be on TV/iPlayer")
            print()
    
    if non_broadcast_matches:
        print("=== NON-BROADCAST ACTS (Festival Only) ===")
        
        for match in non_broadcast_matches:
            print(f"* {match['lineup_artist']}")
            print(f"   {match['stage']} - {match['day']} at {match['time']}")
            print(f"   [FESTIVAL ONLY] Not broadcast")
            print()
    
    # Create summary files
    if broadcast_matches or non_broadcast_matches:
        # Broadcast schedule
        if broadcast_matches:
            with open('broadcast_schedule.txt', 'w', encoding='utf-8') as f:
                f.write("GLASTONBURY 2025 - YOUR BROADCAST SCHEDULE\\n")
                f.write("=" * 50 + "\\n\\n")
                
                current_day = None
                for match in broadcast_matches:
                    if match['day'] != current_day:
                        f.write(f"\\n{match['day'].upper()}\\n")
                        f.write("-" * len(match['day']) + "\\n")
                        current_day = match['day']
                    
                    f.write(f"{match['time']} - {match['lineup_artist']} @ {match['stage']}\\n")
            
            print(f"Broadcast schedule saved to: broadcast_schedule.txt")
        
        # Complete schedule
        all_matches = broadcast_matches + non_broadcast_matches
        with open('complete_festival_schedule.txt', 'w', encoding='utf-8') as f:
            f.write("GLASTONBURY 2025 - COMPLETE SCHEDULE\\n")
            f.write("=" * 50 + "\\n\\n")
            
            f.write("BROADCAST ACTS (TV/iPlayer)\\n")
            f.write("-" * 30 + "\\n")
            for match in broadcast_matches:
                f.write(f"{match['day']} {match['time']} - {match['lineup_artist']} @ {match['stage']}\\n")
            
            f.write("\\nNON-BROADCAST ACTS (Festival Only)\\n")
            f.write("-" * 35 + "\\n")
            for match in non_broadcast_matches:
                f.write(f"{match['day']} {match['time']} - {match['lineup_artist']} @ {match['stage']}\\n")
        
        print(f"Complete schedule saved to: complete_festival_schedule.txt")
        
        # Fix any literal \n characters in the files
        fix_file_formatting('broadcast_schedule.txt')
        fix_file_formatting('complete_festival_schedule.txt')

def fix_file_formatting(filename):
    """Fix literal \n characters in text files"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace literal \n with actual line breaks
        if '\\n' in content:
            fixed_content = content.replace('\\n', '\n')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"Fixed formatting in {filename}")
    except Exception as e:
        print(f"Could not fix {filename}: {e}")

if __name__ == "__main__":
    main()