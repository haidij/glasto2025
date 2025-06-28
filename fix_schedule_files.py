def fix_file(filename):
    """Fix literal \n characters in text files"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace literal \n with actual line breaks
    fixed_content = content.replace('\\n', '\n')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed {filename}")

# Fix both files
fix_file('broadcast_schedule.txt')
fix_file('complete_festival_schedule.txt')
print("Files fixed!")