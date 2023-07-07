import sys
import yaml

def modify_yaml_file(input_file, new_url):
    # Read the YAML file preserving the nested objects
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file, Loader=yaml.Loader)

    # Modify the desired part
    data['servers'][0]['url'] = new_url

    # Convert the modified data back to YAML format
    modified_yaml = yaml.dump(data)

    # Write the modified YAML to 'openapi_resolved.yaml'
    with open('openapi-resolved.yaml', 'w') as file:
        file.write(modified_yaml)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python modify_yaml.py input.yaml new_url')
        sys.exit(1)

    input_file = sys.argv[1]
    new_url = sys.argv[2]

    modify_yaml_file(input_file, new_url)
