import re

def lang_detected(text):
    geez_pattern = re.compile(r'[\u1200-\u137F]')
    latin_pattern = re.compile(r'[a-zA-Z]')
    
    geez_chars = len(geez_pattern.findall(text))
    latin_chars = len(latin_pattern.findall(text))
    total = geez_chars + latin_chars
    
    if total == 0:
        return ['Single', 'English']
    
    geez_ratio = geez_chars / total
    latin_ratio = latin_chars / total
    
    if geez_ratio > 0.7:
        return ['Pure', 'Amharic']
    elif latin_ratio > 0.7:
        return ['Pure', 'English']
    else:
        return ['Mixed', 'English' if latin_ratio >= geez_ratio else 'Amharic']
