import itertools
import re

def is_valid(username):
    """Check if username has at least one letter and valid underscore position"""
    has_letter = any(c.isalpha() for c in username)
    valid_underscore = (username.count('_') == 0) or \
                      (username[1] == '_' and len(username) == 3)
    return has_letter and valid_underscore

def generate_roblox_usernames():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    
    for combo in itertools.product(chars, repeat=3):
        username = ''.join(combo)
        if is_valid(username):
            yield username

with open('name.txt', 'w') as f:
    count = 0
    for username in generate_roblox_usernames():
        f.write(f"{username}\n")
        count += 1
        if count % 100000 == 0:
            print(f"Generated {count:,} valid usernames...")

print(f"\nFinished! Created {count:,} usernames with:")
