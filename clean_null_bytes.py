import os

def clean_null_bytes(directory):
    """Remove null bytes from all Python files in the directory."""
    files_cleaned = []
    
    for root, dirs, files in os.walk(directory):
        # Skip virtual environment directories
        if 'venv' in root or '.venv' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                    
                    if b'\x00' in content:
                        # Remove null bytes
                        cleaned_content = content.replace(b'\x00', b'')
                        with open(filepath, 'wb') as f:
                            f.write(cleaned_content)
                        files_cleaned.append(filepath)
                        print(f"Cleaned: {filepath}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    return files_cleaned

if __name__ == "__main__":
    cleaned = clean_null_bytes('.')
    print(f"\nTotal files cleaned: {len(cleaned)}")
    if cleaned:
        print("\nCleaned files:")
        for f in cleaned:
            print(f"  - {f}")
