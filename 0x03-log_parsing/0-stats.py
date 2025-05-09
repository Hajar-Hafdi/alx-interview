#!/usr/bin/python3
import sys
import re
from signal import signal, SIGINT

# Initialize metrics
total_size = 0
status_counts = {
    200: 0,
    301: 0,
    400: 0,
    401: 0,
    403: 0,
    404: 0,
    405: 0,
    500: 0
}
line_count = 0

# Regular expression pattern to match the input format
pattern = re.compile(
    r'^\S+ - \[\S+ \S+\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)$'
)


def print_stats():
    """Print the accumulated statistics."""
    print(f"File size: {total_size}")
    for status in sorted(status_counts.keys()):
        if status_counts[status] > 0:
            print(f"{status}: {status_counts[status]}")


def signal_handler(sig, frame):
    """Handle keyboard interrupt (CTRL + C)."""
    print_stats()
    sys.exit(0)


# Register the signal handler for keyboard interrupt
signal(SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line = line.strip()
        match = pattern.match(line)
        if match:
            status = int(match.group(1))
            file_size = int(match.group(2))
            
            # Update metrics
            total_size += file_size
            if status in status_counts:
                status_counts[status] += 1
            line_count += 1
            
            # Print stats every 10 lines
            if line_count % 10 == 0:
                print_stats()
except Exception:
    pass
finally:
    # Print stats at the end (in case of normal termination)
    print_stats()
