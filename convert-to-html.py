import re
from datetime import datetime
import os

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Usage example
file_name = "bug_buckets.txt"
search_directory = "/home/runner/work/restler/restler/Fuzz/RestlerResults"

file_path = find_file(file_name, search_directory)
    
with open(file_path, 'r') as file:
    content = file.readlines()
    bug_type = None
    bug_info = ''

output = ''

# find the host
match = re.search(r'Host:\s*([\w.-]+)', ''.join(content))
if match:
    host = match.group(1)
else:
    print("Host part not found.")

# Find the project name from the endpoint summary
project_name_match = re.search(r'\/([^\/]+)\/', ''.join(content))
if project_name_match:
    project_name = project_name_match.group(1)
else:
    project_name = 'Unknown'  # Set a default project name if not found

endpoint_summary_lines = []
error_summary_lines = []
bug_summary_lines = []
bug_data = []

is_endpoint_summary = False
is_error_summary = False
is_bug_body = False

for line in content:
    if line.startswith('Endpoint summary:'):
        is_endpoint_summary = True
        is_error_summary = False
        is_bug_body = False
        continue
    elif line.startswith('Error Code summary:'):
        is_endpoint_summary = False
        is_error_summary = True
        is_bug_body = False
        continue
    elif line.strip() == '-------------':
        is_endpoint_summary = False
        is_error_summary = False
        is_bug_body = True
        continue

    if is_endpoint_summary:
        endpoint_summary_lines.append(line.strip())
    elif is_error_summary:
        error_summary_lines.append(line.strip())
    elif is_bug_body:
        bug_summary_lines.append(line.strip())
        continue

# Style the header of the page
output = '<h1 style="text-align: center; font-family: Arial, sans-serif; color: #333333;">Host: Microsoft RESTler report</h1>'
output += f'<h3 style="text-align: center; font-family: Arial, sans-serif; color: #333333;">Stateful REST API Fuzzing Tool</h3>'
output += f'<h3 style="font-family: Arial, sans-serif; color: #333333;">Host: {host}</h3>'
output += f'<h3 style="font-family: Arial, sans-serif; color: #333333;">Project: {project_name}</h3>'
output += f'<h4 style="font-family: Arial, sans-serif; color: #555555;">For full bug coverage and replays, head to /Fuzz/RestlerResults/experimentxxxx/bug_buckets</h5>'


current_datetime = datetime.now()
current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
output += f'<h5 style="font-family: Arial, sans-serif; color: #777777;">Generated {current_datetime_str}</h5>'
# Add Endpoint summary text with styled header
output += '<div style="margin-bottom: 16px;">'
output += '<p style="font-size: 20px; font-weight: bold; font-family: Arial, sans-serif; color: #333333;">Endpoint Summary:</p>'
output += '<table style="width: auto;">'
output += '<tr>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Method</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Endpoint</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Count</th>'
output += '</tr>'

for line in endpoint_summary_lines:
    parts = line.split(':')
    if len(parts) == 3:
        method = parts[0].strip()
        endpoint = parts[1].strip()
        count = parts[2].strip()
        # Create table row with styled cells
        output += '<tr>'
        output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{method}</td>'
        output += f'<td style="background-color: #E0E0E0; font-family: Arial, sans-serif;">{endpoint}</td>'
        output += f'<td style="background-color: #D0D0D0; font-family: Arial, sans-serif;">{count}</td>'
        output += '</tr>'

output += '</table>'
output += '</div>'

# Add Error Code summary text with styled header
output += '<div style="margin-bottom: 16px;">'
output += '<p style="font-size: 20px; font-weight: bold; font-family: Arial, sans-serif; color: #333333;">Error Code Summary:</p>'
output += '<table style="width: auto;">'
output += '<tr>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Error Code</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Count</th>'
output += '</tr>'

for line in error_summary_lines:
    parts = line.split(':')
    if len(parts) == 2:
        error_code = parts[0].strip()
        count = parts[1].strip()
        # Create table row with styled cells
        output += '<tr>'
        output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{error_code}</td>'
        output += f'<td style="background-color: #D0D0D0; font-family: Arial, sans-serif;">{count}</td>'
        output += '</tr>'

output += '</table>'
output += '</div>'

# Add bug body text with styled header and methods
output += '<div style="margin-bottom: 16px;">'
output += '<p style="font-size: 20px; font-weight: bold; font-family: Arial, sans-serif; color: #333333;">Individual Bugs:</p>'
output += '<table style="width: auto;">'
output += '<tr>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Bug Type</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Methods</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">URL</th>'
output += '<th style="background-color: #000000; color: #FFFFFF; font-family: Arial, sans-serif;">Request</th>'
output += '</tr>'

for line in bug_summary_lines:
    if line.startswith('--------'):
        if bug_type is not None:
            bug_data.append((bug_type, method, url, bug_info))
            bug_type = None
            bug_info = ''
            method = ''
            url = ''
    elif not line.startswith('Hash:'):
        if bug_type is None:
            bug_type = line.strip()
        else:
            match = re.search(r'^(GET|POST|PUT|DELETE)', line)
            if match:
                method = match.group(1)
            line =  re.sub(r'\b(GET|PUT|DELETE|POST)\b', '', line)
            match_url = re.search(r'(/[\w./?=& ]+?)(?=[\s?])', line)
            if match_url:
                url = match_url.group(1)
                url = re.sub(r'[_]', r'<br>', url)  # Add line break after underscores
            else:
                url = "Not Found"
            bug_info += line

for bug_type, method, url, bug_info in bug_data:
    output += '<tr>'
    output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{bug_type}</td>'
    output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{method}</td>'
    output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{url}</td>'
    output += f'<td style="background-color: #F0F0F0; font-family: Arial, sans-serif;">{bug_info}</td>'
    output += '</tr>'

output += '</table>'
output += '</div>'

html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>RESTler Report Summary</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            font-size: 14px;
        }}

        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background-color: #000000;
            color: #FFFFFF;
        }}

        div {{
            margin-top: 16px;
        }}
    </style>
</head>
<body>
    {output}
</body>
</html>
'''

# Save HTML to a file
with open('output.html', 'w') as file:
    file.write(html)
