# This script will be provide both the popular web browsers and malicious site data. It  will take a few
# minutes to populate if ran but it runs a successful report. Out of the 129,952 lines it was able to generate
#11489 lines of possible malicious traffic. 

import re
from collections import Counter

# Reading the log data from the file
with open('lb.log', 'r') as f:
    log_data = f.read()

# Extracting user agents from the log data
user_agents = re.findall(r'"([^"]*)"', log_data)

# Extracting browsers and their versions from user agents
browser_versions = []
for user_agent in user_agents:
    if 'Mozilla' in user_agent:
        match = re.search(r'(?P<browser>Firefox|Chrome|Internet Explorer)[/\s](?P<version>\d+\.\d+|\d+)', user_agent)
        if match:
            browser = match.group('browser')
            version = match.group('version')
            browser_versions.append((browser, version))

# This counts the occurrences of each browser version
browser_version_counts = Counter(browser_versions)

# This will sort the browsers and their versions by count in descending order
sorted_browser_version_counts = sorted(browser_version_counts.items(), key=lambda x: x[1], reverse=True)

# This portion of the script will generate our report
report = "Report: Most Popular Browsers and Their Versions\n"
for i, (browser_version, count) in enumerate(sorted_browser_version_counts):
    report += f"{i+1}. Browser: {browser_version[0]}, Version: {browser_version[1]}, Count: {count}\n"

# This will find our  HTTP error codes in the log data
http_error_codes = []
for line in log_data.split('\n'):
    if re.search(r'\d{3}\s+\d+', line):
        http_error_codes.append(line)

# This portion of the script will add the HTTP error codes to the report
if http_error_codes:
    report += "\nReport: HTTP Error Codes Found\n"
    for i, line in enumerate(http_error_codes):
        report += f"{i+1}. {line}\n"
else:
    report += "\nReport: No HTTP Error Codes Found\n"

# Finding malicious lines in the log data
malicious_lines = []
for line in log_data.split('\n'):
    if re.search(r'(?i)(cmd|sh|bash|wget|curl|ftp)', line):
        malicious_lines.append(line)

# This portion of the script will add the malicious lines to the report
if malicious_lines:
    report += "\nReport: Malicious Traffic Found\n"
    for i, line in enumerate(malicious_lines):
        report += f"{i+1}. {line}\n"
else:
    report += "\nReport: No Malicious Traffic Found\n"

# We'll be writing  the report to a file
with open('report.txt', 'w') as f:
    f.write(report)

print("Report generated successfully!")

