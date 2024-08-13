#!/usr/bin/python3
import sys
import signal
import re

# Global variables to store statistics
total_size = 0
status_codes_count = {
    200: 0,
    301: 0,
    400: 0,
    401: 0,
    403: 0,
    404: 0,
    405: 0,
    500: 0
}

log_line_regex = re.compile(
    r'^\S+ - \[\S+ \S+\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)$'
)

def print_stats():
    """ Function to print the accumulated statistics """
    print("File size: {}".format(total_size))
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print("{}: {}".format(code, status_codes_count[code]))

def parse_line(line):
    """ Function to parse a single line and update statistics """
    global total_size
    match = log_line_regex.match(line)
    
    if match:
        status_code = int(match.group(1))
        file_size = int(match.group(2))

        # Update total size
        total_size += file_size

        # Update status code count if it's a recognized code
        if status_code in status_codes_count:
            status_codes_count[status_code] += 1

def signal_handler(sig, frame):
    """ Signal handler for keyboard interruption (Ctrl + C) """
    print_stats()
    sys.exit(0)

# Register the signal handler for Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

# Process input line by line
line_count = 0
for line in sys.stdin:
    parse_line(line.strip())
    line_count += 1

    # Print stats every 10 lines
    if line_count == 10:
        print_stats()
        line_count = 0

# If the script ends naturally, print any remaining stats
print_stats()
