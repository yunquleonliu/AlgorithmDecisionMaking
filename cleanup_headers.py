
import os
import re

def clean_redundant_headers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    modified = False
    
    while i < len(lines):
        line = lines[i]
        
        # Check if line is a header with potential inline translation
        # Regex: ^(#+)\s+(.*?)(\s*\([A-Za-z0-9\s:,\.-]+\))\s*$
        # Matches: "### Text (English Text)"
        match = re.search(r'^(#+)\s+(.*?)(\s*\([A-Za-z0-9\s:,\.\'-]+\))\s*$', line)
        
        redundancy_found = False
        if match:
            level = match.group(1)
            zh_text = match.group(2)
            en_part_with_parens = match.group(3)
            
            # Look ahead for the next non-empty line
            j = i + 1
            next_line = None
            while j < len(lines):
                if lines[j].strip():
                    next_line = lines[j]
                    break
                j += 1
            
            if next_line:
                # Check if next line is a header of the same level (or similar) AND is English
                # Heuristic: Starts with same # of hashes, and has English characters, no Chinese
                next_header_match = re.search(r'^(#+)\s+(.*)', next_line)
                
                if next_header_match:
                    next_content = next_header_match.group(2)
                    has_zh_next = bool(re.search(r'[\u4e00-\u9fa5]', next_content))
                    
                    if not has_zh_next:
                        # Found redundant pair!
                        # Line i: ZH (EN)
                        # Line k: EN
                        # Action: Remove (EN) from Line i
                        print(f"Cleaning in {os.path.basename(file_path)}:")
                        print(f"  - '{line.strip()}'")
                        print(f"  + Because of: '{next_line.strip()}'")
                        
                        # Reconstruct line: level + space + zh_text + newline
                        new_line = f"{level} {zh_text.strip()}\n"
                        new_lines.append(new_line)
                        redundancy_found = True
                        modified = True
        
        if not redundancy_found:
            new_lines.append(line)
        
        i += 1
        
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

# Scan directory
workspace = r"d:\SyncWork\composition\Algorithm for Future Leaders"
for filename in os.listdir(workspace):
    if filename.endswith(".md"):
        clean_redundant_headers(os.path.join(workspace, filename))
