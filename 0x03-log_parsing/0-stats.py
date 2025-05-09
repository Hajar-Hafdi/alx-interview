"""Log parsing script - computes metrics from stdin input."""
import sys
import signal

# Initialize counters
total_size = 0
status_counts = {}
valid_codes = ['200', '301', '400', '401', '403', '404', '405', '500']
line_count = 0


def print_stats():
    """Print the accumulated metrics."""
    print("File size: {}".format(total_size))
    for code in sorted(status_counts.keys()):
        print("{}: {}".format(code, status_counts[code]))


try:
    for line in sys.stdin:
        line = line.strip()
        line_count += 1
        parts = line.split()

        # Validate line structure
        if len(parts) >= 7 and parts[-2] in valid_codes:
            try:
                status = parts[-2]
                file_size = int(parts[-1])
                total_size += file_size
                if status in status_counts:
                    status_counts[status] += 1
                else:
                    status_counts[status] = 1
            except ValueError:
                pass  # Skip lines with invalid file size

        if line_count % 10 == 0:
            print_stats()

except KeyboardInterrupt:
    print_stats()
    raise

# Final stats print after reading all input
print_stats()
