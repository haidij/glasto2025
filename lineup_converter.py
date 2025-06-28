import json
import re

def parse_lineup_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lineup = {}
    current_stage = None
    current_day = None
    
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a stage/day header
        if ' - ' in line and ('Friday' in line or 'Saturday' in line or 'Sunday' in line or 'Thursday' in line):
            parts = line.split(' - ')
            if len(parts) == 2:
                current_stage = parts[0].strip()
                current_day = parts[1].strip()
                
                if current_stage not in lineup:
                    lineup[current_stage] = {}
                if current_day not in lineup[current_stage]:
                    lineup[current_stage][current_day] = []
        
        # Check if it's an artist/time entry
        elif ':' in line and ' - ' in line and current_stage and current_day:
            # Match pattern like "Artist Name: 12:00 - 13:00"
            match = re.match(r'^(.+?):\s*(\d{2}:\d{2}\s*-\s*\d{2}:\d{2}).*$', line)
            if match:
                artist = match.group(1).strip()
                time = match.group(2).strip()
                
                lineup[current_stage][current_day].append({
                    'artist': artist,
                    'time': time
                })
    
    return lineup

# Convert the lineup
lineup_json = parse_lineup_to_json('2025lineup.md')

# Save to JSON file
with open('glastonbury_2025_lineup.json', 'w', encoding='utf-8') as f:
    json.dump(lineup_json, f, indent=2, ensure_ascii=False)

print("Lineup converted to JSON format!")
print(f"Found {len(lineup_json)} stages")
for stage, days in lineup_json.items():
    total_artists = sum(len(artists) for artists in days.values())
    print(f"  {stage}: {len(days)} days, {total_artists} artists")