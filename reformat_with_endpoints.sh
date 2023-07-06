#!/bin/bash
input_file=$(find /home/runner/work/restler/restler/Fuzz/RestlerResults -name "bug_buckets.txt" -type f)

# Extract lines containing the endpoints
endpoints=$(grep -oE '(POST|GET|PUT|HEAD|DELETE) .+' "$input_file" | awk '{print $1 " " $2}' | cut -d'?' -f1)

# Trim leading and trailing spaces from each endpoint
endpoints=$(echo "$endpoints" | awk '{$2=$2;print}')

# Count the occurrences of each unique endpoint
count=$(echo "$endpoints" | sort | uniq -c)

# Generate the output with counts
output=$(echo "$count" | awk '{ printf "%s: %s: %d\n", $2, $3, $1 }')

# Print the result
echo -e "Endpoint Summary: \n$output\n\nError Code Summary:" | cat - "$input_file" > output.txt
mv output.txt "$input_file"
