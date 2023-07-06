import json

# Path to the JSON file
file_path = '/var/lib/jenkins/workspace/RESTler/Compile/engine_settings.json'

# Read the JSON file
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Modify the JSON content
json_data['per_resource_settings'] = {}
json_data['max_combinations'] = 20
json_data['authentication']['token']['location'] = '/var/lib/jenkins/workspace/RESTler/access_token.txt'
json_data['authentication']['token']['token_refresh_interval'] = 300
json_data['max_request_execution_time'] = 90
json_data['max_async_resource_creation_time'] = 60
json_data['global_producer_timing_delay'] = 2
json_data['time_budget'] = 0.25

# Write the modified JSON back to the file
with open(file_path, 'w') as file:
    json.dump(json_data, file, indent=4)
