import sys
import ruamel.yaml

def modify_yaml_file(input_file, new_url):
    # Read the YAML file
    with open(input_file, 'r') as file:
        data = ruamel.yaml.round_trip_load(file)

    # Modify the desired part
    data['servers'][0]['url'] = new_url

    # Convert the modified data back to YAML format
    ruamel.yaml.round_trip_dump(data, open('openapi-resolved.yaml', 'w'))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python modify_yaml.py input.yaml new_url')
        sys.exit(1)

    input_file = sys.argv[1]
    new_url = sys.argv[2]

    modify_yaml_file(input_file, new_url)
