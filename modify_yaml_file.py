import sys
import yaml

def find_and_replace_url(file_path, new_url):
    # Read the YAML file
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Find and update the URL within the "servers" section
    servers = data.get('servers', [])
    for server in servers:
        if 'url' in server:
            server['url'] = new_url

    # Write the modified YAML back to the file
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# Check if the correct number of arguments are provided
if len(sys.argv) < 3:
    print("Usage: python modify_yaml_file.py <file_path> <new_url>")
    sys.exit(1)

# Retrieve the file path and new URL from command-line arguments
file_path = sys.argv[1]
new_url = sys.argv[2]

# Call the function to find and replace the URL
find_and_replace_url(file_path, new_url)
