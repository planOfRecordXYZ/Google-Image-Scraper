import os
import argparse
import uuid

# Set up argument parser to get the search key and new name prefix from command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search-key', help='the folder name for scraping images', required=True)
parser.add_argument('-t', '--token_name', help='the filename to use when storing the files. I.e. tokenname "jwa" will store files "jwa (1).jpg", "jwa (2).jpg" and so on. this has no effect if --keep-filenames is True', required=True)

args = parser.parse_args()

# Print the provided search key and new name prefix
print(f'Search key: {args.search_key}')
print(f'New name prefix: {args.token_name}')

# Construct the path to the photos directory
photos_dir = os.path.join('photos', args.search_key)

# Check if the directory exists
if not os.path.exists(photos_dir):
    print(f'Directory {photos_dir} does not exist')
    exit(1)
    
# Get a list of all files in the directory
files = sorted((f for f in os.listdir(photos_dir) if not f.startswith(".")), key=str.lower)

# Rename each file, 1st pass
for file in files:
    # Get the file name and extension
    name, ext = os.path.splitext(file)

    # Generate a unique UUID for the file
    uuid_str = str(uuid.uuid4())

    # Construct the new file name
    new_name = f'{args.token_name}_{uuid_str}{ext}'

    # Rename the file
    os.rename(os.path.join(photos_dir, file), os.path.join(photos_dir, new_name))

# Get a list of all files in the directory
files = sorted((f for f in os.listdir(photos_dir) if not f.startswith(".")), key=str.lower)

# In the second pass, rename the files to the desired format
for i, file in enumerate(files):
    # Get the file name and extension
    name, ext = os.path.splitext(file)

    # Construct the new file name
    new_name = f'{args.token_name} ({i+1}){ext}'

    # Rename the file
    os.rename(os.path.join(photos_dir, file), os.path.join(photos_dir, new_name))

print('Done')
