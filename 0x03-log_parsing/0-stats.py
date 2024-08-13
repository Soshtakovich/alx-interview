#!/usr/bin/python3
import sys
import signal

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

def print_stats():
    """ Function to print the accumulated statistics """
    print("File size: {}".format(total_size))
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print("{}: {}".format(code, status_codes_count[code]))

def parse_line(line):
    """ Function to parse a single line and update statistics """
    global total_size
    parts = line.split()
    
    # Validate line format
    if len(parts) < 7 or parts[5] != '"GET' or parts[6] != '/projects/260':
        return

    try:
        # Extract status code and file size
        status_code = int(parts[8])
        file_size = int(parts[9])

        # Update total size
        total_size += file_size

        # Update status code count if it's a recognized code
        if status_code in status_codes_count:
            status_codes_count[status_code] += 1
    except (ValueError, IndexError):
        pass

def signal_handler(sig, frame):
    """ Signal handler for keyboard interruption (Ctrl + C) """
    print_stats()
    sys.exit(0)

# Register the signal handler for Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

# Process input line by line
line_count = 0
for line in sys.stdin:
    parse_line(line)
    line_count += 1

    # Print stats every 10 lines
    if line_count == 10:
        print_stats()
        line_count = 0

# If the script ends naturally, print any remaining stats
print_stats()
